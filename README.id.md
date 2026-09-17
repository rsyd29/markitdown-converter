# MarkItDown Converter

[English](README.md) | **Bahasa Indonesia**

Aplikasi CLI sederhana untuk mengonversi file **PDF, PowerPoint, Word, Excel**,
serta berbagai format lain menjadi **Markdown**, memanfaatkan pustaka
[`markitdown`](https://github.com/microsoft/markitdown) dari Microsoft.

## Fitur

- Konversi banyak format: PDF, PPTX, DOCX, XLSX/XLS, CSV, HTML, XML, JSON,
  TXT, RTF, ODT, ODP, ODS, EPUB, Outlook (msg), gambar, audio, dan lainnya.
- UI interaktif berbasis CLI — cukup masukkan path file.
- Pilih bahasa antarmuka (Indonesia atau Inggris) saat aplikasi dijalankan.
- Hasil Markdown bisa diberi nama kustom, atau otomatis memakai nama file
  sumber dengan ekstensi diganti menjadi `.md`.
- Menangani file yang tidak ditemukan, konversi gagal, dan konfirmasi
  penimpaan bila file hasil sudah ada.

## Persyaratan

- Python 3.11 atau lebih baru
- `pip`

## Instalasi

```bash
cd markitdown-converter

# Buat virtual environment (bila belum ada)
python3 -m venv .venv

# Aktifkan virtual environment
source .venv/bin/activate

# Pasang dependency
pip install -r requirements.txt
```

> Virtual environment (`.venv`) sudah dibuat pada project ini. Bila sudah ada,
> cukup aktifkan dengan `source .venv/bin/activate`.

> Dependency di atas mencakup format dokumen utama (PDF, Word, PowerPoint,
> Excel, dan Outlook) serta transkripsi audio (`audio-transcription`). Format
> dasar lain (CSV, HTML, XML, JSON, TXT, EPUB, dll.) sudah didukung tanpa
> dependency tambahan.
>
> File audio (`.wav`, `.mp3`, `.m4a`, `.mp4`) juga memerlukan:
> - [`ffmpeg`](https://ffmpeg.org/) tersedia di `PATH` (mis. `brew install ffmpeg`)
>
> Audio ditranskripsi lewat layanan suara Google per potongan 60 detik dengan
> percobaan ulang otomatis. Jika layanan itu tidak terjangkau (mis. error
> broken pipe), aplikasi otomatis beralih ke model
> [Whisper](https://github.com/openai/whisper) lokal (`faster-whisper`) yang
> berjalan sepenuhnya offline.
>
> Jika perlu fitur lain, kamu bisa menambahkan extras lain, contoh:
> - `youtube-transcription` — transkripsi video YouTube
> - `az-doc-intel` / `az-content-understanding` — layanan Azure (butuh kredensial)
> - atau `markitdown[all]` untuk memasang semuanya sekaligus

## Cara Menjalankan

Pastikan dependency sudah terpasang (lihat [Instalasi](#instalasi)).

### Mulai cepat

```bash
./run.sh
```

Skrip ini membuat virtual environment (bila perlu), memasang dependency, lalu
menjalankan aplikasi.

### macOS / Linux

```bash
# Aktifkan virtual environment, lalu jalankan
source .venv/bin/activate
python main.py
```

Atau langsung tanpa mengaktifkan venv:

```bash
.venv/bin/python main.py
```

Karena `main.py` sudah executable dan punya shebang, cara ini juga bisa:

```bash
source .venv/bin/activate
./main.py
```

### Windows

```bash
# Aktifkan virtual environment (Command Prompt / PowerShell)
.venv\Scripts\activate
python main.py
```

Atau langsung tanpa mengaktifkan venv:

```bash
.venv\Scripts\python.exe main.py
```

Lalu ikuti langkahnya:

1. Pilih bahasa antarmuka: `1` untuk Bahasa Indonesia, `2` untuk English.
2. Masukkan path file yang ingin diubah, contoh:
   - `report.pdf`
   - `presentasi.pptx`
   - `/Users/nama/Documents/dokumen.docx`
3. Program akan mengonversi file dan menampilkan jumlah karakter hasil.
4. Pilih penamaan file hasil:
   - `1` → nama sama dengan sumber (hanya ekstensi berubah jadi `.md`)
   - `2` → nama/path kustom (bila hanya nama, disimpan di folder sumber)
5. File Markdown tersimpan. Program kembali meminta file berikutnya.

Ketik `q` kapan saja untuk keluar.

## Struktur

```
markitdown-converter/
├── main.py           # Program utama (CLI)
├── i18n.py           # Teks terjemahan (Indonesia/Inggris)
├── run.sh            # Skrip setup & jalankan sekali perintah
├── requirements.txt  # Dependency
├── README.md         # Dokumentasi (Inggris)
├── README.id.md      # Dokumentasi (Indonesia)
└── LICENSE           # Lisensi MIT
```

## Troubleshooting

- **Editor menampilkan "Import markitdown could not be resolved"** — package
  `markitdown` sudah terpasang di environment. Muat ulang language server Python
  (di Zed: `Cmd+Shift+P` → *language server: restart*, atau *Reload Window*)
  agar index-nya diperbarui.
- **Audio gagal dengan error koneksi (broken pipe/timeout)** — aplikasi
  otomatis beralih ke Whisper lokal. Bila keduanya gagal, cek koneksi internet,
  VPN/proxy, atau firewall, dan pastikan `faster-whisper` terpasang.
- **Audio menghasilkan hasil kosong atau tanpa transkrip** — pasang dependency
  audio (`pip install "markitdown[audio-transcription]"`) dan pastikan `ffmpeg`
  ada di `PATH`. File tanpa suara jelas (musik, hening) tidak bisa ditranskripsi.
- **File tidak terkonversi untuk format tertentu** — pastikan extras yang
  relevan terpasang (lihat bagian Instalasi).

## Lisensi

Dirilis di bawah [Lisensi MIT](LICENSE).
