#!/usr/bin/env python3
"""
Web Interface untuk LSTM Medical Chatbot
Flask web app untuk chatbot medis dengan model LSTM
"""

from flask import Flask, render_template, request, jsonify, session
import pickle
import numpy as np
import re
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'medical_chatbot_secret_key'

class LSTMWebChatbot:
    def __init__(self):
        self.model = None
        self.word_to_index = None
        self.label_encoder = None
        self.max_length = 100
        self.response_generator = MedicalResponseGenerator()
        
    def load_model_and_data(self):
        """Load model dan data yang diperlukan"""
        try:
            # Load processed data
            with open('processed_data/medical_data.pkl', 'rb') as f:
                data = pickle.load(f)
            
            self.word_to_index = data['word_to_index']
            self.label_encoder = data['label_encoder']
            self.max_length = data['max_length']
            
            # Load trained model
            import tensorflow as tf
            self.model = tf.keras.models.load_model('models/lstm_chatbot_model.h5')
            
            print("🔄 Loading processed data...")
            print("✅ Processed data loaded successfully")
            print("🔄 Loading LSTM model...")
            print("✅ LSTM model loaded successfully")
            print("✅ Model dan data berhasil dimuat!")
            return True
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False
    
    def preprocess_text(self, text):
        """Simple text preprocessing"""
        # Remove punctuation and convert to lowercase
        processed_text = re.sub(r'[^\w\s]', '', text.lower())
        return processed_text
    
    def text_to_sequence(self, text, word_to_index, max_length):
        """Convert text to sequence"""
        words = text.split()
        sequence = []
        
        for word in words:
            if word in word_to_index:
                sequence.append(word_to_index[word])
            else:
                sequence.append(0)  # Unknown word
        
        # Pad sequence
        if len(sequence) < max_length:
            sequence.extend([0] * (max_length - len(sequence)))
        else:
            sequence = sequence[:max_length]
        
        return sequence
    
    def predict_intent(self, text):
        """Predict intent dari input text"""
        # Preprocess text
        processed_text = self.preprocess_text(text)
        sequence = self.text_to_sequence(processed_text, self.word_to_index, self.max_length)
        
        # Predict
        prediction = self.model.predict(np.array([sequence]), verbose=0)
        intent_idx = np.argmax(prediction[0])
        confidence = np.max(prediction[0])
        
        intent = self.label_encoder.inverse_transform([intent_idx])[0]
        
        return intent, confidence
    
    def extract_patient_info(self, text, intent):
        """Extract patient information from text"""
        text_lower = text.lower()
        patient_info = {}
        
        # Always try to extract name regardless of intent if it contains name-related keywords
        name_keywords = ['nama', 'perkenalkan', 'panggil', 'saya']
        if any(keyword in text_lower for keyword in name_keywords):
            # Extract name with more flexible patterns
            name_patterns = [
                r'nama\s+(?:saya\s+)?(?:adalah\s+)?([a-zA-Z\s]+)',
                r'perkenalkan\s+(?:nama\s+)?(?:saya\s+)?([a-zA-Z\s]+)',
                r'panggil\s+(?:saya\s+)?([a-zA-Z\s]+)',
                r'saya\s+(?:nama\s+)?([a-zA-Z\s]+)',
                r'nama\s+([a-zA-Z\s]+)',
                r'([a-zA-Z\s]+)\s+(?:nama\s+)?saya'
            ]
        else:
            # If no name keywords found, check if the entire text might be a name
            # This handles cases like just "nugroho", "budi", etc.
            text_clean = text.strip()
            # Only treat as name if it's short (max 15 chars) and doesn't contain symptom keywords or negative responses
            symptom_keywords = ['pilek', 'pusing', 'demam', 'batuk', 'sakit', 'nyeri', 'mual', 'muntah']
            negative_responses = ['tidak', 'tidak ada', 'tidak ada', 'no', 'none', 'kosong']
            
            if (len(text_clean) > 0 and len(text_clean) <= 15 and 
                text_clean.replace(' ', '').isalpha() and
                not any(symptom in text_lower for symptom in symptom_keywords) and
                not any(negative in text_lower for negative in negative_responses)):
                # If text is short, alphabetic, no symptom keywords, and not negative response, treat as name
                name_patterns = [r'^([a-zA-Z\s]+)$']
            else:
                name_patterns = []
        
        # Extract name using patterns
        for pattern in name_patterns:
            match = re.search(pattern, text_lower)
            if match:
                patient_info['name'] = match.group(1).strip().title()
                break
        
        # Extract age
        age_pattern = r'(\d+)\s*(?:tahun|thn)'
        age_match = re.search(age_pattern, text_lower)
        if age_match:
            patient_info['age'] = age_match.group(1)
        
        # Handle symptoms extraction - always check for symptoms regardless of intent
        symptom_keywords = [
            'demam', 'panas', 'batuk', 'pilek', 'sakit kepala', 'pusing',
            'mual', 'muntah', 'sakit perut', 'nyeri', 'lemas', 'kelelahan',
            'sesak nafas', 'nyeri dada', 'nyeri otot', 'pegal', 'gatal'
        ]
        
        found_symptoms = []
        for symptom in symptom_keywords:
            if symptom in text_lower:
                found_symptoms.append(symptom)
        
        if found_symptoms:
            patient_info['symptoms'] = found_symptoms
        
        return patient_info
    
    def generate_response(self, intent, user_input, session_data):
        """Generate response berdasarkan intent"""
        # Extract patient info
        patient_info = self.extract_patient_info(user_input, intent)
        
        # Update session data
        if 'patient_data' not in session_data:
            session_data['patient_data'] = {
                'name': '',
                'age': '',
                'symptoms': [],
                'medical_history': [],
                'conversation_stage': 'greeting'  # Track conversation stage
            }
        
        # Update patient data
        if 'name' in patient_info:
            session_data['patient_data']['name'] = patient_info['name']
        if 'age' in patient_info:
            session_data['patient_data']['age'] = patient_info['age']
        if 'symptoms' in patient_info:
            session_data['patient_data']['symptoms'].extend(patient_info['symptoms'])
            # Remove duplicates
            session_data['patient_data']['symptoms'] = list(set(session_data['patient_data']['symptoms']))
        
        # Generate response
        patient_name = session_data['patient_data']['name'] if session_data['patient_data']['name'] else "Pasien"
        symptoms_text = ', '.join(session_data['patient_data']['symptoms']) if session_data['patient_data']['symptoms'] else None
        
        # Determine the appropriate intent based on extracted information and conversation stage
        text_lower = user_input.lower()
        negative_responses = ['tidak', 'tidak ada', 'no', 'none', 'kosong']
        is_negative_response = any(negative in text_lower for negative in negative_responses)
        
        # Get current conversation stage
        current_stage = session_data['patient_data'].get('conversation_stage', 'greeting')
        
        # Check if we should end the conversation
        if current_stage == 'diagnosis_complete':
            intent = 'goodbye'
        elif is_negative_response and (current_stage == 'symptoms_confirmed' or session_data['patient_data']['symptoms']):
            # If negative response after symptoms confirmed, end conversation with final diagnosis
            intent = 'diagnosis'
            session_data['patient_data']['conversation_stage'] = 'diagnosis_complete'
        elif patient_info.get('symptoms'):
            # If we extracted symptoms, provide diagnosis
            if current_stage == 'symptoms_confirmed':
                # If symptoms already confirmed, provide final diagnosis
                intent = 'diagnosis'
                session_data['patient_data']['conversation_stage'] = 'diagnosis_complete'
            else:
                # First time symptoms detected
                intent = 'symptoms'
                session_data['patient_data']['conversation_stage'] = 'symptoms_confirmed'
        elif patient_info.get('name') and intent == 'general':
            # If we have a name but no age yet, ask for age
            if not session_data['patient_data']['age']:
                intent = 'biodata'
                session_data['patient_data']['conversation_stage'] = 'name_provided'
            else:
                # If we have both name and age, ask for symptoms
                intent = 'age'
                session_data['patient_data']['conversation_stage'] = 'age_provided'
        elif patient_info.get('age') and intent == 'general':
            # If we extracted age, ask for symptoms
            intent = 'age'
            session_data['patient_data']['conversation_stage'] = 'age_provided'
        elif is_negative_response:
            # If it's a negative response, continue with the conversation flow
            if session_data['patient_data']['symptoms']:
                # If we already have symptoms, provide final diagnosis
                intent = 'diagnosis'
                session_data['patient_data']['conversation_stage'] = 'diagnosis_complete'
            else:
                # If no symptoms yet, ask for symptoms
                intent = 'negative_response'
        
        response = self.response_generator.generate_response(
            intent, user_input, patient_name, symptoms_text
        )
        
        return response, session_data['patient_data']

class MedicalResponseGenerator:
    def __init__(self):
        self.response_templates = {
            'greeting': [
                "Halo! Selamat datang di layanan kesehatan kami. Saya siap membantu Anda dengan diagnosis penyakit. Boleh saya ketahui nama Anda?",
                "Hai! Selamat datang di chatbot kesehatan. Saya akan membantu menganalisis gejala Anda. Bisa tolong berikan nama Anda?",
                "Selamat datang! Saya adalah asisten kesehatan yang siap membantu. Mari kita mulai dengan data pribadi Anda."
            ],
            'biodata': [
                "Terima kasih {name}. Berapa usia Anda?",
                "Baik {name}, bisa tolong berikan usia Anda?",
                "Terima kasih atas informasinya {name}. Berapa tahun usia Anda?"
            ],
            'age': [
                "Terima kasih {name}. Sekarang, bisakah Anda jelaskan gejala yang sedang Anda alami?",
                "Baik {name}, sekarang saya perlu tahu gejala apa yang Anda rasakan saat ini?",
                "Terima kasih atas informasinya {name}. Bisa tolong ceritakan keluhan kesehatan Anda?"
            ],
            'symptoms': [
                "Saya mengerti gejala Anda. Berdasarkan gejala tersebut, kemungkinan diagnosis adalah {diagnosis}. Apakah ada gejala lain?",
                "Terima kasih atas penjelasannya. Gejala yang Anda sebutkan mengarah ke {diagnosis}. Sudah berapa lama gejala ini muncul?",
                "Saya mencatat gejala Anda. Kemungkinan besar Anda mengalami {diagnosis}. Apakah ada riwayat penyakit sebelumnya?"
            ],
            'medical_history': [
                "Terima kasih atas informasi riwayat medis Anda. Ini akan membantu dalam diagnosis yang lebih akurat.",
                "Saya mencatat riwayat medis Anda. Apakah ada obat yang sedang Anda konsumsi saat ini?",
                "Baik, riwayat medis Anda sudah saya catat. Sekarang, apakah ada gejala lain yang ingin Anda sampaikan?"
            ],
            'medication': [
                "Saya mencatat obat yang Anda konsumsi. Apakah ada efek samping yang Anda rasakan?",
                "Terima kasih atas informasi obat Anda. Apakah ada alergi terhadap obat tertentu?",
                "Baik, saya sudah mencatat obat Anda. Sekarang, bagaimana dengan gejala yang Anda alami?"
            ],
            'diagnosis': [
                "Berdasarkan gejala dan informasi yang Anda berikan, kemungkinan diagnosis adalah {diagnosis}. Saya sarankan untuk berkonsultasi dengan dokter untuk pemeriksaan lebih lanjut. Terima kasih telah menggunakan layanan kami!",
                "Setelah menganalisis gejala Anda, kemungkinan Anda mengalami {diagnosis}. Untuk diagnosis yang lebih akurat, silakan berkonsultasi dengan dokter. Semoga lekas sembuh!",
                "Diagnosis sementara berdasarkan gejala Anda adalah {diagnosis}. Namun, tetap disarankan untuk pemeriksaan medis langsung. Terima kasih telah menggunakan layanan kesehatan kami!"
            ],
            'goodbye': [
                "Terima kasih telah menggunakan layanan kami. Semoga lekas sembuh!",
                "Selamat tinggal! Jangan lupa untuk selalu menjaga kesehatan Anda.",
                "Terima kasih! Jika ada keluhan lain, jangan ragu untuk kembali ke sini."
            ],
            'general': [
                "Maaf, saya tidak sepenuhnya memahami maksud Anda. Bisa tolong jelaskan lebih detail?",
                "Mohon maaf, bisa tolong dijelaskan lebih lanjut tentang keluhan Anda?",
                "Saya ingin memastikan saya memahami dengan benar. Bisa tolong ulangi atau jelaskan lebih detail?"
            ],
            'negative_response': [
                "Baik, saya mengerti. Sekarang, bisakah Anda jelaskan gejala yang sedang Anda alami?",
                "Terima kasih atas informasinya. Bisa tolong ceritakan keluhan kesehatan Anda?",
                "Baik, sekarang saya perlu tahu gejala apa yang Anda rasakan saat ini?"
            ]
        }
        
        self.disease_mapping = {
            'demam': ['Common Cold', 'Influenza', 'COVID-19', 'Dengue Fever'],
            'panas': ['Common Cold', 'Influenza', 'COVID-19', 'Dengue Fever'],
            'batuk': ['Bronchitis', 'Pneumonia', 'Asthma', 'Common Cold'],
            'pilek': ['Common Cold', 'Sinusitis', 'Allergic Rhinitis'],
            'sakit kepala': ['Migraine', 'Tension Headache', 'Hypertension', 'Sinusitis'],
            'pusing': ['Migraine', 'Tension Headache', 'Vertigo', 'Anemia'],
            'mual': ['Gastritis', 'Food Poisoning', 'Migraine', 'Pregnancy'],
            'muntah': ['Gastritis', 'Food Poisoning', 'Migraine', 'Gastroenteritis'],
            'sakit perut': ['Gastritis', 'Ulcer', 'Appendicitis', 'Kidney Stones'],
            'nyeri': ['Inflammation', 'Injury', 'Infection', 'Chronic Pain'],
            'lemas': ['Anemia', 'Depression', 'Chronic Fatigue Syndrome', 'Diabetes'],
            'kelelahan': ['Anemia', 'Depression', 'Chronic Fatigue Syndrome', 'Diabetes'],
            'sesak nafas': ['Asthma', 'Pneumonia', 'Heart Disease', 'Anxiety'],
            'nyeri dada': ['Heart Disease', 'Angina', 'Pneumonia', 'Anxiety'],
            'nyeri otot': ['Flu', 'Dengue', 'Arthritis', 'Fibromyalgia'],
            'pegal': ['Flu', 'Dengue', 'Arthritis', 'Fibromyalgia'],
            'gatal': ['Allergic Reaction', 'Skin Infection', 'Eczema', 'Contact Dermatitis']
        }
    
    def generate_response(self, intent, user_input="", patient_name="", symptoms=None):
        """Generate response berdasarkan intent"""
        import random
        
        if intent in self.response_templates:
            template = random.choice(self.response_templates[intent])
            
            # Replace placeholders
            if '{name}' in template and patient_name:
                template = template.replace('{name}', patient_name)
            
            if '{diagnosis}' in template and symptoms:
                # Simple diagnosis based on symptoms
                diagnosis = self.simple_diagnosis(symptoms)
                template = template.replace('{diagnosis}', diagnosis)
            
            return template
        else:
            return random.choice(self.response_templates['general'])
    
    def simple_diagnosis(self, symptoms):
        """Simple diagnosis berdasarkan gejala"""
        if not symptoms:
            return "penyakit umum"
        
        # Convert symptoms to lowercase for matching
        symptoms_lower = symptoms.lower()
        
        for symptom_key, diseases in self.disease_mapping.items():
            if symptom_key in symptoms_lower:
                import random
                return random.choice(diseases)
        
        return "penyakit umum"

# Initialize chatbot
chatbot = LSTMWebChatbot()

@app.route('/')
def index():
    """Main page"""
    return render_template('lstm_index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Pesan tidak boleh kosong'})
        
        # Predict intent
        intent, confidence = chatbot.predict_intent(user_message)
        
        # Generate response
        response, patient_data = chatbot.generate_response(intent, user_message, session)
        
        # Update session
        session['patient_data'] = patient_data
        
        # Get the final intent that was actually used for response generation
        final_intent = intent
        if patient_data.get('symptoms') and intent == 'medical_history':
            final_intent = 'symptoms'
        
        # Prepare response data
        response_data = {
            'response': response,
            'intent': final_intent,
            'confidence': float(confidence),
            'timestamp': datetime.now().strftime('%H:%M'),
            'patient_data': patient_data
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({'error': 'Terjadi kesalahan dalam memproses pesan'})

@app.route('/reset', methods=['POST'])
def reset_chat():
    """Reset chat session"""
    session.clear()
    return jsonify({'message': 'Chat berhasil direset'})

@app.route('/patient_data', methods=['GET'])
def get_patient_data():
    """Get current patient data"""
    patient_data = session.get('patient_data', {})
    return jsonify(patient_data)

if __name__ == '__main__':
    print("🚀 Starting LSTM Medical Chatbot Web Interface...")
    
    # Load model and data
    if not chatbot.load_model_and_data():
        print("❌ Gagal memuat model. Pastikan model sudah di-training.")
        exit(1)
    
    print("📱 Access the chatbot at: http://localhost:5001")
    
    # Check if running in production
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(debug=debug, host='0.0.0.0', port=port) 