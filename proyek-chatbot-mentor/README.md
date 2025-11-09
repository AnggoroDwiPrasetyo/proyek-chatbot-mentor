# 🧑‍🔬 Mentor Data Science (Pro)

Chatbot interaktif yang dibangun dengan Streamlit dan Google Gemini. Berperan sebagai "Mentor Data Science" yang ramah, chatbot ini dapat menjawab pertanyaan-pertanyaan *advanced* dan mendaftarkan pengguna ke kursus menggunakan *Function Calling*.

## Getting Started

### Prerequisites

Pastikan Anda telah menginstal Python. Sangat disarankan untuk menggunakan `miniconda` atau `conda` untuk manajemen lingkungan.

### Installation

1.  **Instal Miniconda (jika belum punya)**

    Unduh dan instal Miniconda dari situs resminya:
    <https://docs.conda.io/en/latest/miniconda.html>

2.  **Buat Lingkungan Conda**

    Buka terminal atau Anaconda Prompt Anda dan buat lingkungan baru (kita akan menamakannya `mentorbot`):

    ```bash
    conda create -n mentorbot python=3.10
    conda activate mentorbot
    ```

3.  **Install Dependensi**

    Navigasi ke direktori proyek Anda dan instal paket yang diperlukan:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Dapatkan Google API Key**

    Proyek ini memerlukan Google API Key untuk terhubung ke model Gemini.
    * Dapatkan key Anda secara gratis dari [Google AI Studio](https://aistudio.google.com/app/apikey).
    * Key ini akan dimasukkan di sidebar aplikasi saat dijalankan.

5.  **Jalankan Aplikasi Streamlit**

    ```bash
    streamlit run streamlit_app.py
    ```

    Aplikasi akan terbuka di browser web Anda di `http://localhost:8501`.

## Code Structure

* **streamlit_app.py**: File aplikasi utama Streamlit. Berisi semua logika UI, CSS kustom, persona bot, definisi *tool* (`enroll_in_course`), dan alur obrolan.
* **requirements.txt**: Mendaftar semua dependensi Python (`streamlit` dan `google-generativeai`) yang diperlukan untuk proyek ini.