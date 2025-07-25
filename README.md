# Medical Chatbot LSTM System

Sistem chatbot kesehatan berbasis LSTM (Long Short-Term Memory) yang dapat melakukan diagnosis penyakit berdasarkan gejala pasien. Sistem ini menggunakan dataset medis dari Kaggle dan model deep learning untuk memahami intent dan memberikan respons yang tepat.

## 🏥 Fitur Utama

- **Intent Classification**: Menggunakan model LSTM untuk mengklasifikasikan intent dari input user
- **Medical Diagnosis**: Diagnosis penyakit berdasarkan gejala yang dilaporkan
- **Conversation Management**: Manajemen alur percakapan yang terstruktur
- **Web Interface**: Antarmuka web yang user-friendly
- **Console Interface**: Antarmuka console untuk testing
- **Comprehensive Evaluation**: Evaluasi model yang lengkap dengan berbagai metrik

## 📊 Dataset

Sistem menggunakan dataset medis dari Kaggle:
- [Medical Diagnosis using Patient Profile Dataset](https://www.kaggle.com/code/sonualexantony/medical-diagnosis-using-patient-profile-dataset/input)
- Dataset tambahan untuk mencapai 2000+ records
- Data sintetis untuk augmentasi dataset

## 🏗️ Arsitektur Sistem

```
Medical Chatbot LSTM
├── Data Collection (data_collector.py)
├── Data Preprocessing (data_preprocessing.py)
├── LSTM Model (lstm_model.py)
├── Chatbot Engine (medical_chatbot.py)
├── Web Interface (web_interface.py)
├── Model Evaluation (model_evaluation.py)
└── Main Controller (main.py)
```

## 🚀 Instalasi

### 1. Clone Repository
```bash
git clone <repository-url>
cd medical-chatbot-lstm
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Kaggle API (Optional)
Jika ingin menggunakan dataset Kaggle asli:
```bash
# Install kaggle CLI
pip install kaggle

# Setup kaggle credentials
# Download kaggle.json dari Kaggle account settings
# Place it in ~/.kaggle/kaggle.json
```

## 🎯 Penggunaan

### Mode Lengkap (Recommended)
```bash
python main.py --mode full
```

### Mode Individual
```bash
# Setup direktori
python main.py --mode setup

# Pengumpulan data
python main.py --mode collect

# Preprocessing data
python main.py --mode preprocess

# Training model
python main.py --mode train

# Evaluasi model
python main.py --mode evaluate

# Web interface
python main.py --mode web

# Console interface
python main.py --mode console
```

### Skip Data Collection
```bash
python main.py --mode full --skip-data
```

## 📁 Struktur File

```
medical-chatbot-lstm/
├── main.py                     # Script utama
├── requirements.txt            # Dependencies
├── README.md                   # Dokumentasi
├── data_collector.py          # Pengumpulan data
├── data_preprocessing.py      # Preprocessing data
├── lstm_model.py              # Model LSTM
├── medical_chatbot.py         # Engine chatbot
├── web_interface.py           # Web interface
├── model_evaluation.py        # Evaluasi model
├── datasets/                  # Dataset mentah
├── processed_data/            # Data yang sudah diproses
├── models/                    # Model yang sudah ditrain
├── evaluation_results/        # Hasil evaluasi
├── templates/                 # HTML templates
│   └── index.html
└── static/                    # Static files
    ├── css/
    │   └── style.css
    └── js/
        └── chatbot.js
```

## 🤖 Cara Kerja Sistem

### 1. Data Collection
- Mengumpulkan dataset dari Kaggle
- Membuat data sintetis untuk augmentasi
- Menggabungkan semua dataset

### 2. Data Preprocessing
- Tokenisasi dan normalisasi teks
- Penghapusan stop words
- Lemmatization
- Pembuatan vocabulary
- Konversi teks ke sequence

### 3. Model Training
- Model LSTM dengan embedding layer
- Bidirectional LSTM layers
- Dropout untuk regularisasi
- Dense layers untuk classification

### 4. Intent Classification
- Greeting: Sapaan awal
- Biodata: Informasi pasien
- Symptoms: Gejala yang dialami
- Medical History: Riwayat medis
- Medication: Obat yang dikonsumsi
- Diagnosis: Diagnosis penyakit
- Goodbye: Perpisahan

### 5. Response Generation
- Template-based responses
- Dynamic content insertion
- Context-aware responses

## 📊 Evaluasi Model

### Metrik yang Digunakan
- **Accuracy**: Akurasi klasifikasi
- **Precision**: Presisi per kelas
- **Recall**: Recall per kelas
- **F1-Score**: F1-score per kelas
- **Confusion Matrix**: Matriks kebingungan
- **Cross-Validation**: Validasi silang

### Hasil Evaluasi
Hasil evaluasi disimpan di `evaluation_results/`:
- `evaluation_report.md`: Laporan evaluasi lengkap
- `confusion_matrix.png`: Visualisasi confusion matrix
- `metrics_comparison.png`: Perbandingan metrik
- `training_history.png`: Grafik training history

## 🌐 Web Interface

### Fitur Web Interface
- **Real-time Chat**: Percakapan real-time
- **Patient Data Panel**: Panel data pasien
- **Symptoms Tracking**: Pelacakan gejala
- **Diagnosis Display**: Tampilan diagnosis
- **Model Info**: Informasi model (intent, confidence, state)
- **Responsive Design**: Desain responsif

### Akses Web Interface
```bash
python main.py --mode web
# Buka browser: http://localhost:5000
```

## 💬 Console Interface

### Fitur Console Interface
- **Interactive Chat**: Percakapan interaktif
- **Real-time Feedback**: Feedback real-time
- **Debug Information**: Informasi debug

### Akses Console Interface
```bash
python main.py --mode console
```

## 🔧 Konfigurasi

### Parameter Model
```python
# lstm_model.py
vocab_size = 10000          # Ukuran vocabulary
max_length = 100           # Panjang maksimal sequence
embedding_dim = 128        # Dimensi embedding
lstm_units = 128          # Unit LSTM
```

### Parameter Training
```python
# lstm_model.py
epochs = 30               # Jumlah epoch
batch_size = 32          # Batch size
learning_rate = 0.001    # Learning rate
```

## 📈 Performa Model

### Hasil Training
- **Accuracy**: ~95% (tergantung dataset)
- **Training Time**: ~10-15 menit (CPU)
- **Model Size**: ~50-100 MB

### Optimasi
- Early stopping untuk mencegah overfitting
- Dropout layers untuk regularisasi
- Bidirectional LSTM untuk capture context
- Learning rate scheduling

## 🚨 Disclaimer

⚠️ **PENTING**: Sistem ini hanya untuk tujuan edukasi dan demonstrasi. Diagnosis yang diberikan adalah diagnosis sementara dan tidak menggantikan konsultasi dengan dokter profesional. Selalu konsultasikan dengan dokter untuk diagnosis yang akurat.

## 🤝 Kontribusi

Kontribusi sangat diterima! Silakan:
1. Fork repository
2. Buat feature branch
3. Commit changes
4. Push ke branch
5. Buat Pull Request

## 📝 License

MIT License - lihat file LICENSE untuk detail.

## 📞 Support

Jika ada pertanyaan atau masalah:
- Buat issue di GitHub
- Email: [your-email@example.com]
- Dokumentasi lengkap: [link-to-docs]

## 🔄 Changelog

### v1.0.0 (2024-01-XX)
- Initial release
- LSTM-based intent classification
- Web and console interfaces
- Comprehensive evaluation
- Medical diagnosis system

---

**Dibuat dengan ❤️ untuk layanan kesehatan yang lebih baik** # Updated for Railway deployment
