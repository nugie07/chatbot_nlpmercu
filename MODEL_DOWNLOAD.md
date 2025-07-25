# 📥 Download Model dan Data

## File yang Diperlukan

Untuk menjalankan chatbot, Anda perlu file-file berikut:

### 1. Model Files
- `models/lstm_chatbot_model.h5` - Model LSTM yang sudah di-training
- `models/best_lstm_model.h5` - Model terbaik (backup)

### 2. Processed Data
- `processed_data/medical_data.pkl` - Data yang sudah diproses (word_to_index, label_encoder, max_length)

### 3. Dataset Files (Opsional)
- `datasets/combined_medical_dataset.csv` - Dataset gabungan
- `datasets/synthetic_medical_data.csv` - Data sintetis

## Cara Mendapatkan File

### Opsi 1: Training Ulang Model
```bash
# Jalankan notebook untuk training
python3 -m jupyter notebook chatbot_main.ipynb

# Atau jalankan script training
python3 lstm_model.py
```

### Opsi 2: Download dari Google Drive
File model tersedia di Google Drive:
- [Model Files](https://drive.google.com/drive/folders/...)
- [Processed Data](https://drive.google.com/drive/folders/...)

### Opsi 3: Generate Data Sintetis
```bash
# Generate dataset sintetis
python3 data_collector.py
python3 data_preprocessing.py
```

## Struktur Folder Setelah Download

```
chatbot/
├── models/
│   ├── lstm_chatbot_model.h5
│   └── best_lstm_model.h5
├── processed_data/
│   └── medical_data.pkl
├── datasets/
│   └── synthetic_medical_data.csv
└── ... (file lainnya)
```

## Verifikasi File

Setelah download, pastikan file ada dengan menjalankan:

```bash
ls -la models/
ls -la processed_data/
```

## Troubleshooting

### Error: Model tidak ditemukan
- Pastikan file `models/lstm_chatbot_model.h5` ada
- Pastikan file `processed_data/medical_data.pkl` ada

### Error: Dataset tidak ditemukan
- Jalankan `python3 data_collector.py` untuk generate data sintetis
- Atau download dataset dari sumber yang disediakan 