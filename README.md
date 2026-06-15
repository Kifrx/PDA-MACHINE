# PDA Simulator Machine
| Name           | NRP        | 
| ---            | ---        | 
| Rafi Attar Maulana | 5025241141 | 
| Syah Amin Zikri | 5025241197 | 
| Davin Adiputra Suryolaksana | 5025241220 |


## Deskripsi
Program akan membaca string yang dimasukkan pengguna dan menentukan apakah string tersebut **Accepted** atau **Rejected** berdasarkan aturan keseimbangan kurung menggunakan struktur data stack.

Kurung yang didukung:

* `()`
* `[]`
* `{}`

---

## Fitur

### 1. Single String Testing

Pengguna dapat menguji satu string dan melihat:

* Trace proses PDA
* Isi stack pada setiap langkah
* Status Accepted / Rejected
* Statistik stack

### 2. Multi String Testing

Pengguna dapat menguji beberapa string sekaligus (satu string per baris).

### 3. Stack Trace

Program menampilkan setiap operasi PDA seperti:

* PUSH
* POP
* ERROR

beserta kondisi stack setelah setiap operasi.

### 4. Statistik Stack

Program menampilkan:

* Input Length
* Total Push
* Total Pop
* Maximum Stack Depth
* Final Stack Depth

---

## Requirements

* Python 3.x

## Cara Menjalankan Program

1. Pastikan Python telah terinstal.

2. Simpan file program, misalnya:

```bash
pda_simulator.py
```

3. Jalankan program:

```bash
python pda_simulator.py
```

atau

```bash
python3 pda_simulator.py
```

4. Jendela GUI akan muncul.

---

## Aturan Input

Program hanya menerima karakter berikut:

```text
(
)
[
]
{
}
```

Karakter selain yang tercantum di atas akan dianggap tidak valid dan menghasilkan status REJECT.

---

## Contoh Input Valid

### Contoh 1

```text
()
```

Hasil:

```text
ACCEPT
```

---

### Contoh 2

```text
([]{})
```

Hasil:

```text
ACCEPT
```

---

### Contoh 3

```text
{[()]}
```

Hasil:

```text
ACCEPT
```

---

### Contoh 4

```text
(((([[]]))))
```

Hasil:

```text
ACCEPT
```

---

## Contoh Input Tidak Valid

### Contoh 1

```text
([)]
```

Hasil:

```text
REJECT
```

Karena urutan penutupan kurung tidak sesuai.

---

### Contoh 2

```text
((]
```

Hasil:

```text
REJECT
```

Karena kurung yang ditutup tidak cocok dengan kurung yang dibuka.

---

### Contoh 3

```text
(()))
```

Hasil:

```text
REJECT
```

Karena terdapat kurung tutup berlebih.

---

### Contoh 4

```text
((()
```

Hasil:

```text
REJECT
```

Karena masih terdapat kurung buka yang belum ditutup.

---

## Cara Menggunakan Multi String Testing

Masukkan satu string pada setiap baris.

Contoh:

```text
([])
([)]
{[()]}
(((
```

Output:

```text
1  ([])     ACCEPT
2  ([)]     REJECT
3  {[()]}   ACCEPT
4  (((      REJECT
```

---

## Konsep PDA yang Digunakan

Program menggunakan:

* Satu state utama untuk membaca input
* Stack sebagai memori
* Operasi PUSH untuk kurung buka
* Operasi POP untuk kurung tutup yang sesuai

String akan diterima (ACCEPT) jika:

1. Semua simbol berhasil diproses.
2. Tidak terjadi kesalahan pencocokan kurung.
3. Stack kembali ke simbol awal (`Z0`) setelah seluruh input dibaca.


