# 🚀 Panduan Deployment Medical LSTM Chatbot

## Platform Deployment Gratis

### 1. Railway (Rekomendasi Utama)

**Keunggulan:**
- ✅ Gratis untuk project kecil
- ✅ Mudah digunakan
- ✅ Mendukung Python/Flask
- ✅ Auto-deploy dari GitHub
- ✅ SSL otomatis

**Cara Deploy:**

1. **Buat akun Railway:**
   - Kunjungi [railway.app](https://railway.app)
   - Sign up dengan GitHub

2. **Upload ke GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/username/repo-name.git
   git push -u origin main
   ```

3. **Deploy di Railway:**
   - Klik "New Project"
   - Pilih "Deploy from GitHub repo"
   - Pilih repository Anda
   - Railway akan otomatis detect Flask app

4. **Set Environment Variables (opsional):**
   - `FLASK_ENV=production`
   - `PORT=5001`

### 2. Render

**Keunggulan:**
- ✅ Gratis tier tersedia
- ✅ Auto-deploy dari GitHub
- ✅ Custom domain support

**Cara Deploy:**

1. **Buat akun Render:**
   - Kunjungi [render.com](https://render.com)
   - Sign up dengan GitHub

2. **Deploy:**
   - Klik "New Web Service"
   - Connect GitHub repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `gunicorn lstm_web_interface:app`
   - Deploy

### 3. Heroku (Alternatif)

**Keunggulan:**
- ✅ Platform yang sudah established
- ✅ Banyak add-ons

**Keterbatasan:**
- ❌ Tidak lagi gratis untuk hobby projects
- ❌ Perlu credit card untuk verifikasi

## File yang Sudah Disiapkan

✅ `Procfile` - Untuk deployment
✅ `runtime.txt` - Versi Python
✅ `requirements.txt` - Dependencies + gunicorn
✅ `.gitignore` - File yang diignore
✅ `lstm_web_interface.py` - Updated untuk production

## Troubleshooting

### Error: Model tidak ditemukan
- Pastikan file `models/lstm_chatbot_model.h5` ada
- Pastikan file `processed_data/medical_data.pkl` ada

### Error: Port binding
- Railway/Render akan set PORT environment variable
- Kode sudah diupdate untuk menggunakan `os.environ.get('PORT', 5001)`

### Error: Dependencies
- Pastikan semua dependencies ada di `requirements.txt`
- Gunicorn sudah ditambahkan untuk production server

## Testing Setelah Deploy

1. **Test Basic Functionality:**
   ```bash
   curl -X POST https://your-app.railway.app/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "Halo"}'
   ```

2. **Test Web Interface:**
   - Buka URL yang diberikan platform
   - Test conversation flow

## Monitoring

- Railway: Dashboard built-in
- Render: Logs dan metrics tersedia
- Set up alerts untuk error

## Cost Optimization

- Railway: Free tier cukup untuk testing
- Render: Free tier dengan sleep mode
- Monitor usage untuk avoid charges 