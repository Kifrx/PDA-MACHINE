# Web-Based PDA Simulator Machine

| Nama | NRP |
| --- | --- |
| Rafi Attar Maulana | 5025241141 |
| Syah Amin Zikri | 5025241197 |
| Davin Adiputra Suryolaksana | 5025241220 |

## Deskripsi

Proyek ini adalah simulator *Pushdown Automaton* (PDA) interaktif berbasis web untuk mengenali Bahasa Kurung Seimbang:

$$L = \{w \mid w \text{ memiliki jumlah dan urutan kurung () yang seimbang}\}$$

Aplikasi dirancang menggunakan arsitektur modern yang memisahkan **Python HTTP Server (Backend)** sebagai mesin pemroses transisi/logika automata dan **HTML5/JS (Frontend)** sebagai antarmuka visualisasi dinamis.

---

## Arsitektur Sistem

Aplikasi berjalan menggunakan dua komponen utama yang harus diletakkan dalam satu direktori:

* **`pda.py` (Backend):** Server HTTP bawaan Python yang menyediakan REST API di `/api/simulate` untuk menghasilkan *trace state* berformat JSON, serta meng-host file statis.
* **`pda_simulator.html` (Frontend):** Antarmuka web UI yang merender animasi stack, diagram transisi SVG, *input tape*, dan tabel riwayat interaktif menggunakan MathJax dan CSS modern.

---

## Fitur Utama

### 1. Visualisasi Interaktif Step-by-Step

Pengguna dapat mengontrol jalannya penelusuran string secara manual menggunakan tombol **Step Forward (Maju)**, **Step Backward (Mundur)**, atau menggunakan fitur **Auto Play** dengan kecepatan eksekusi yang dapat diatur via slider.

### 2. Representasi Memori Stack Dinamis

Setiap operasi `PUSH` (saat membaca `(`) dan `POP` (saat membaca `)`) divisualisasikan secara langsung melalui komponen grafis tabung stack vertikal lengkap dengan animasi transisi elemen.

### 3. Diagram Transisi SVG & Input Tape Live

* Mendeteksi posisi pembacaan karakter (*Input Tape*) saat ini.
* Menyoroti (*highlighting*) *state* yang sedang aktif (`q0` atau `qf`) serta jalur transisi yang sedang dieksekusi langsung pada diagram mesin grafis.

### 4. Tabel Riwayat & Jump-to-Step

Menampilkan seluruh log konfigurasi transisi formal dari langkah awal hingga akhir. Pengguna dapat langsung melompat (*jump*) ke urutan langkah tertentu hanya dengan mengklik baris pada tabel riwayat.

---

## Requirements

* Python 3.x (Tanpa memerlukan *third-party library* tambahan).
* Browser Modern (Chrome, Edge, Firefox, atau Safari) dengan koneksi internet untuk memuat *engine* perantara LaTeX (MathJax).

---

## Cara Menjalankan Program

Pastikan file `pda.py` dan `pda_simulator.html` berada di dalam **folder yang sama**.

### Mode Web UI (Default)

1. Buka terminal/command prompt di direktori proyek.
2. Jalankan server backend:
    ```bash
    python pda.py
    ```


3. Buka browser Anda dan akses URL: `http://localhost:8080`




---

## Aturan Input & Spesifikasi Transisi

Mesin PDA ini dikonfigurasi secara ketat dengan parameter formal berikut:

* **Alfabet Input ($\Sigma$):** `(` dan `)`
* **Alfabet Stack ($\Gamma$):** `X` dan `Z0` (Simbol dasar)
* **State ($Q$):** `q0` (State Utama) dan `qf` (State Penerima/Final)

### Fungsi Transisi ($\delta$) yang Diterapkan:

* $\delta(q_0, (, Z_0) = (q_0, XZ_0)$ $\rightarrow$ *Push X jika stack kosong*
* $\delta(q_0, (, X) = (q_0, XX)$ $\rightarrow$ *Push X jika stack berisi X*
* $\delta(q_0, ), X) = (q_0, \epsilon)$ $\rightarrow$ *Pop X jika kurung berpasangan*
* $\delta(q_0, \epsilon, Z_0) = (q_f, Z_0)$ $\rightarrow$ *Accept string jika input habis & stack kembali bersih*

> **Catatan:** Karakter selain `(` atau `)` atau kondisi urutan kurung yang salah (misal: top stack kosong saat membaca `)`) akan langsung memicu status **REJECT**.