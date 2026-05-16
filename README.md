# Vector Space Model (VSM) Information Retrieval

Program ini mengimplementasikan Vector Space Model (VSM) untuk sistem temu balik informasi (information retrieval) menggunakan Python. Program akan menerima koleksi dokumen dan query, lalu merepresentasikan keduanya sebagai vektor multidimensi untuk menghitung tingkat kemiripan (cosine similarity).

## Cara Menjalankan Program

1. **Instalasi Dependencies:**
   Pastikan Python 3 sudah terinstal di sistem Anda. Lalu instal library yang dibutuhkan dengan menjalankan perintah berikut di terminal:

   ```bash
   pip install -r requirements.txt
   ```
2. Menjalankan Program:
Program dijalankan melalui command line / terminal dengan argumen nama file base (berisi daftar dokumen) dan nama file query.
Bash

    ```bash 
    python vsm.py base.txt query.txt
    ```
    Sedikit catatan, anda dapat mengganti query.txt dengan query2.txt, query3.txt, dll untuk menguji query yang berbeda.

### Penjelasan Sekilas untuk Algoritma
Program VSM ini bekerja melalui beberapa tahapan berikut:
- Preprocessing: Teks dari dokumen dan query diproses melalui:
    - **Tokenisasi/Tokenization:** Memecah teks kalimat menjadi kata-kata (token).
    - **Pembersihan/clear:** Menghapus tanda baca dan menghapus stopwords (kata hubung/umum dalam bahasa Inggris).
    - **Stemming:** Mengubah setiap kata ke bentuk dasarnya (misal: "retrieval" menjadi "retriev") menggunakan metode Porter Stemmer.
    - **Perhitungan Bobot (TF-IDF):** 
      - **TF (Term Frequency):** Menghitung frekuensi kemunculan setiap term dalam dokumen, dihitung menggunakan logaritmik ($1 + \log(TF)$).
      - **IDF (Inverse Document Frequency):** Menghitung tingkat kepentingan suatu term. Semakin jarang kata muncul di dokumen lain, semakin tinggi nilai IDF-nya.
      - **TF-IDF:** Mengalikan bobot TF dan IDF.
    - **Cosine Similarity:** Program mengubah setiap dokumen dan query menjadi representasi vektor berdasarkan bobot TF-IDF. Kemudian program menghitung tingkat kemiripan antara dokumen dan query menggunakan Cosine Similarity (mengukur nilai kosinus sudut antar vektor). Dokumen kemudian akan diurutkan berdasarkan skor kemiripan dari yang paling tinggi ke rendah.

## Contoh Hasil Keluaran Program

Setelah program berhasil dijalankan (misalnya dengan menjalankan `python vsm.py base.txt query.txt`), program akan menghasilkan file keluaran di dalam folder masing-masing:

### 1. File Inverted Index (<u>index/index_query.txt</u>)
Menampilkan daftar seluruh term (yang sudah di-stem) beserta daftar dokumen dan bobot kemunculannya.
Contoh potongan keluaran:

    barcelona: doc1.txt,0.6990
    compet: doc2.txt,0.6990
    cup: doc2.txt,0.6990
    fifa: doc2.txt,0.6990
    florida: doc3.txt,0.6990

### 2. File Bobot (<u>weights/weights_query.txt</u>)
Menampilkan daftar bobot setiap term di masing-masing dokumen.
Contoh potongan keluaran:

    doc2.txt: iran,0.3979 host,0.3979 departur,0.6990 ralli,0.6990 fifa,0.6990 world,0.6990 cup,0.6990 squad,0.6990 wit,0.6990 thousand,0.6990 fan,0.6990 tehran,0.6990 enqelab,0.6990 squar,0.6990 amid,0.6990 concern,0.6990 team,0.6990 travel,0.6990 unit,0.6990 state,0.6990 compet,0.6990

### 3. File Response / Perangkingan (<u>response/response_query.txt</u>)
Menampilkan jumlah dokumen yang relevan (memiliki skor di atas 0.001) beserta nilai kemiripannya yang sudah diurutkan dari yang tertinggi ke terendah.
Contoh keluaran untuk pencarian query.txt ("United States World Cup 2026"):

    1
    doc2.txt 0.4512