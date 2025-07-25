// Medical Chatbot JavaScript
class MedicalChatbot {
    constructor() {
        this.chatMessages = document.getElementById('chatMessages');
        this.messageInput = document.getElementById('messageInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.resetBtn = document.getElementById('resetBtn');
        
        this.isLoading = false;
        
        this.initializeEventListeners();
        this.updateCurrentTime();
        setInterval(() => this.updateCurrentTime(), 1000);
    }
    
    initializeEventListeners() {
        // Send message on button click
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        
        // Send message on Enter key
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Reset conversation
        this.resetBtn.addEventListener('click', () => this.resetConversation());
        
        // Auto-resize input
        this.messageInput.addEventListener('input', () => this.autoResizeInput());
    }
    
    updateCurrentTime() {
        const now = new Date();
        const timeString = now.toLocaleTimeString('id-ID', {
            hour: '2-digit',
            minute: '2-digit'
        });
        
        const timeElements = document.querySelectorAll('.message-time');
        if (timeElements.length > 0) {
            timeElements[timeElements.length - 1].textContent = timeString;
        }
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        
        if (!message || this.isLoading) {
            return;
        }
        
        // Add user message to chat
        this.addMessage(message, 'user');
        
        // Clear input
        this.messageInput.value = '';
        this.autoResizeInput();
        
        // Show loading
        this.showLoading();
        
        try {
            // Send message to server
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            const data = await response.json();
            
            // Hide loading
            this.hideLoading();
            
            if (data.error) {
                this.addMessage('Maaf, terjadi kesalahan dalam sistem. Silakan coba lagi.', 'bot');
            } else {
                // Add bot response
                this.addMessage(data.response, 'bot');
                
                // Update sidebar information
                this.updateSidebar(data);
            }
            
        } catch (error) {
            console.error('Error:', error);
            this.hideLoading();
            this.addMessage('Maaf, terjadi kesalahan dalam sistem. Silakan coba lagi.', 'bot');
        }
    }
    
    addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        const icon = document.createElement('i');
        icon.className = sender === 'user' ? 'fas fa-user' : 'fas fa-robot';
        
        const text = document.createElement('p');
        text.textContent = content;
        
        messageContent.appendChild(icon);
        messageContent.appendChild(text);
        
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = new Date().toLocaleTimeString('id-ID', {
            hour: '2-digit',
            minute: '2-digit'
        });
        
        messageDiv.appendChild(messageContent);
        messageDiv.appendChild(timeDiv);
        
        this.chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        this.scrollToBottom();
    }
    
    showLoading() {
        this.isLoading = true;
        this.sendBtn.disabled = true;
        
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message bot-message';
        loadingDiv.id = 'loadingMessage';
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        const icon = document.createElement('i');
        icon.className = 'fas fa-robot';
        
        const loadingSpinner = document.createElement('div');
        loadingSpinner.className = 'loading';
        
        const text = document.createElement('p');
        text.textContent = 'Sedang memproses...';
        
        messageContent.appendChild(icon);
        messageContent.appendChild(loadingSpinner);
        messageContent.appendChild(text);
        
        loadingDiv.appendChild(messageContent);
        this.chatMessages.appendChild(loadingDiv);
        
        this.scrollToBottom();
    }
    
    hideLoading() {
        this.isLoading = false;
        this.sendBtn.disabled = false;
        
        const loadingMessage = document.getElementById('loadingMessage');
        if (loadingMessage) {
            loadingMessage.remove();
        }
    }
    
    updateSidebar(data) {
        // Update patient data
        if (data.patient_data) {
            const patientData = data.patient_data;
            
            document.getElementById('patientName').textContent = patientData.name || '-';
            document.getElementById('patientAge').textContent = patientData.age || '-';
            document.getElementById('patientGender').textContent = patientData.gender || '-';
            
            // Update symptoms
            this.updateSymptomsList(patientData.symptoms || []);
        }
        
        // Update model info
        document.getElementById('currentIntent').textContent = data.intent || '-';
        document.getElementById('confidenceScore').textContent = data.confidence ? `${(data.confidence * 100).toFixed(1)}%` : '-';
        document.getElementById('currentState').textContent = data.state || '-';
        
        // Update diagnosis if available
        if (data.state === 'diagnosis' && data.patient_data && data.patient_data.symptoms) {
            this.updateDiagnosis(data.patient_data.symptoms);
        }
    }
    
    updateSymptomsList(symptoms) {
        const symptomsList = document.getElementById('symptomsList');
        
        if (symptoms.length === 0) {
            symptomsList.innerHTML = '<p class="no-symptoms">Belum ada gejala yang dilaporkan</p>';
            return;
        }
        
        symptomsList.innerHTML = '';
        
        const symptomMapping = {
            'fever': 'Demam',
            'cough': 'Batuk',
            'headache': 'Sakit Kepala',
            'fatigue': 'Lelah',
            'nausea': 'Mual',
            'chest_pain': 'Nyeri Dada',
            'shortness_of_breath': 'Sesak Napas',
            'abdominal_pain': 'Sakit Perut',
            'dizziness': 'Pusing',
            'joint_pain': 'Nyeri Sendi'
        };
        
        symptoms.forEach(symptom => {
            const symptomDiv = document.createElement('div');
            symptomDiv.className = 'symptom-item';
            symptomDiv.textContent = symptomMapping[symptom] || symptom;
            symptomsList.appendChild(symptomDiv);
        });
    }
    
    updateDiagnosis(symptoms) {
        const diagnosisResult = document.getElementById('diagnosisResult');
        
        if (symptoms.length === 0) {
            diagnosisResult.innerHTML = '<p class="no-diagnosis">Belum ada diagnosis</p>';
            return;
        }
        
        // Simple diagnosis logic
        let diagnosis = 'Penyakit Umum';
        
        if (symptoms.includes('fever') && symptoms.includes('cough')) {
            diagnosis = 'Common Cold / Influenza';
        } else if (symptoms.includes('chest_pain')) {
            diagnosis = 'Kemungkinan Masalah Jantung';
        } else if (symptoms.includes('headache')) {
            diagnosis = 'Migrain / Sakit Kepala Tegang';
        } else if (symptoms.includes('abdominal_pain')) {
            diagnosis = 'Gastritis / Masalah Pencernaan';
        }
        
        diagnosisResult.innerHTML = `<p>${diagnosis}</p>`;
    }
    
    async resetConversation() {
        if (confirm('Apakah Anda yakin ingin mereset percakapan?')) {
            try {
                const response = await fetch('/reset', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Clear chat messages
                    this.chatMessages.innerHTML = '';
                    
                    // Add initial bot message
                    this.addMessage('Halo! Selamat datang di layanan kesehatan kami. Saya adalah asisten kesehatan yang siap membantu Anda dengan diagnosis penyakit berdasarkan dataset medis. Boleh saya ketahui nama Anda?', 'bot');
                    
                    // Reset sidebar
                    this.resetSidebar();
                    
                    // Show success message
                    this.showNotification('Percakapan berhasil direset!', 'success');
                } else {
                    this.showNotification('Gagal mereset percakapan', 'error');
                }
                
            } catch (error) {
                console.error('Error resetting conversation:', error);
                this.showNotification('Gagal mereset percakapan', 'error');
            }
        }
    }
    
    resetSidebar() {
        // Reset patient data
        document.getElementById('patientName').textContent = '-';
        document.getElementById('patientAge').textContent = '-';
        document.getElementById('patientGender').textContent = '-';
        
        // Reset symptoms
        document.getElementById('symptomsList').innerHTML = '<p class="no-symptoms">Belum ada gejala yang dilaporkan</p>';
        
        // Reset diagnosis
        document.getElementById('diagnosisResult').innerHTML = '<p class="no-diagnosis">Belum ada diagnosis</p>';
        
        // Reset model info
        document.getElementById('currentIntent').textContent = '-';
        document.getElementById('confidenceScore').textContent = '-';
        document.getElementById('currentState').textContent = 'greeting';
    }
    
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        // Add styles
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            z-index: 1000;
            animation: slideIn 0.3s ease;
            max-width: 300px;
        `;
        
        // Set background color based on type
        if (type === 'success') {
            notification.style.backgroundColor = '#28a745';
        } else if (type === 'error') {
            notification.style.backgroundColor = '#dc3545';
        } else {
            notification.style.backgroundColor = '#17a2b8';
        }
        
        // Add to page
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }
    
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    autoResizeInput() {
        // Reset height
        this.messageInput.style.height = 'auto';
        
        // Set new height based on content
        const newHeight = Math.min(this.messageInput.scrollHeight, 120);
        this.messageInput.style.height = newHeight + 'px';
    }
}

// Initialize chatbot when page loads
document.addEventListener('DOMContentLoaded', () => {
    const chatbot = new MedicalChatbot();
    
    // Add CSS animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
    
    // Focus on input
    chatbot.messageInput.focus();
    
    // Make chatbot globally accessible for debugging
    window.medicalChatbot = chatbot;
});

// Handle page visibility change
document.addEventListener('visibilitychange', () => {
    if (!document.hidden) {
        // Refocus input when page becomes visible
        const messageInput = document.getElementById('messageInput');
        if (messageInput) {
            messageInput.focus();
        }
    }
});

// Handle beforeunload event
window.addEventListener('beforeunload', (e) => {
    // Optional: Show confirmation dialog when leaving page
    // e.preventDefault();
    // e.returnValue = '';
}); 