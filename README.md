# AcehGPT

AcehGPT adalah asisten kecerdasan buatan (AI) berbasis RAG (Retrieval-Augmented Generation) yang dirancang untuk menjawab pertanyaan dan memberikan informasi seputar sejarah, budaya, dan dokumen kebijakan terkait Aceh secara akurat.

Sistem ini terdiri dari backend FastAPI yang terintegrasi dengan **Turbovec** (mesin pencarian vektor terkompresi 4-bit) dan antarmuka frontend berbasis React.

---

## 🏗️ Arsitektur Sistem

Proyek ini terbagi menjadi dua komponen utama:

1. **Backend (`aceh-gpt-backend/`)**:
   - **FastAPI**: Kerangka kerja API web berkinerja tinggi untuk melayani kueri chat.
   - **Turbovec**: Menggunakan indeks kuantisasi 4-bit (`TurboQuantIndex`) untuk pencarian dokumen berkecepatan tinggi dengan kebutuhan memori minimal.
   - **RAG Pipeline**: Mengambil dokumen relevan dari indeks vektor lalu menyusun konteks untuk dikirim ke model bahasa (LLM) untuk menghasilkan respons yang akurat.

2. **Frontend (`frontendChat.md`)**:
   - Antarmuka chat interaktif modern dengan desain premium berbasis TailwindCSS dan Lucide Icons.
   - Menyediakan fitur input teks, saran kueri pencarian dokumen, animasi pengetikan (*typing indicator*), dan riwayat chat.

---

## 📁 Struktur Direktori

```text
AcehGPT/
├── aceh-gpt-backend/        # Kode sumber backend Python
│   ├── app/                 # Aplikasi FastAPI utama
│   │   ├── api/             # Endpoint & rute API (Chat & Health)
│   │   ├── services/        # Logika bisnis RAG dan Vector Database
│   │   └── config.py        # Pengaturan & konfigurasi lingkungan (.env)
│   ├── data/                # Dokumen sumber (.txt) untuk diindeks
│   ├── ingest.py            # Skrip pipa ingesti (ingestion pipeline) dokumen
│   ├── main.py              # Titik masuk utama aplikasi FastAPI
│   └── requirements.txt     # Daftar dependency Python
├── frontendChat.md          # Kode komponen React Frontend (Simulasi UI)
└── README.md                # Dokumentasi proyek (File ini)
```

---

## 🚀 Panduan Memulai

### 1. Ingesti Dokumen (Membuat Indeks Vektor)

Sebelum menjalankan server, dokumen teks harus diproses ke dalam indeks vektor menggunakan skrip `ingest.py`.

1. Letakkan dokumen sumber dalam format `.txt` di dalam folder `aceh-gpt-backend/data/`.
2. Jalankan skrip ingesti untuk memproses dokumen dan membuat file indeks vektor `aceh_knowledge.tq`:
   ```bash
   cd aceh-gpt-backend
   python3 ingest.py --data-dir data --index-path aceh_knowledge.tq --mapping-path aceh_knowledge_docs.json
   ```

Skrip ini akan otomatis menghasilkan embedding menggunakan model `sentence-transformers/all-MiniLM-L6-v2` dan menyimpannya menggunakan kompresi 4-bit Turbovec.

### 2. Menjalankan Backend API

Jalankan server pengembangan FastAPI dengan Uvicorn:

```bash
cd aceh-gpt-backend
python3 main.py
```

Server akan berjalan secara default di `http://127.0.0.1:8000`. Anda dapat mengakses dokumentasi API interaktif (Swagger UI) di `http://127.0.0.1:8000/api/v1/docs`.

### 3. Frontend Chat

Komponen frontend diimplementasikan dalam React di file [frontendChat.md](file:///home/sherlock/AcehGPT/frontendChat.md). Kode ini dapat digunakan di dalam proyek React (seperti Vite atau Next.js) dengan menginstal dependency berikut:
```bash
npm install lucide-react
```

---

## 🔒 Konfigurasi Keamanan

Proyek ini dikembangkan dengan mematuhi standar keamanan ketat:
- **CORS Terkontrol**: Menggunakan daftar domain asal tepercaya (`ALLOWED_ORIGINS`) alih-alih wildcard (`*`).
- **Local Listening Only**: Server FastAPI secara bawaan mendengarkan kueri pada `127.0.0.1` dan bukan `0.0.0.0` untuk mencegah eksposur yang tidak disengaja ke jaringan publik.
