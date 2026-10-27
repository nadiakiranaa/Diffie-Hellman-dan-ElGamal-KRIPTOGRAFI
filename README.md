# Diffie-Hellman dan ElGamal: Pengiriman Pesan Rahasia Bob ke Alice

Program studi kasus kriptografi yang menggabungkan **Diffie-Hellman** (kesepakatan kunci sesi) dan **ElGamal** (enkripsi pesan). Seluruh perhitungan dibuat secara manual, **tanpa library atau framework kriptografi jadi**.

Repositori ini berisi dua versi program yang logikanya sama:

1. **Versi Python** untuk dijalankan di terminal.
2. **Versi web** (satu file HTML) yang menampilkan setiap tahap beserta rumus dan nilai antaranya.

---

## Identitas Kelompok

| | |
|---|---|
| Kelompok | Kelompok X |
| Anggota | Nadia Kirana Afifah , Clarissa Aydin Rahmazea, Ananda Widi Alrafi |
| Mata kuliah | Kriptografi |
| Topik | Diffie-Hellman dan ElGamal (Pertemuan 9) |

Ganti isi tabel di atas dengan data kelompok yang sebenarnya.

---

## Daftar Isi

1. [Studi Kasus](#studi-kasus)
2. [Isi Repositori](#isi-repositori)
3. [Cara Menjalankan](#cara-menjalankan)
4. [Alur Program](#alur-program)
5. [Rumus yang Dipakai](#rumus-yang-dipakai)
6. [Penjelasan Fungsi pada Kode Python](#penjelasan-fungsi-pada-kode-python)
7. [Cara Teks Diubah Menjadi Angka](#cara-teks-diubah-menjadi-angka)
8. [Verifikasi dengan Contoh Materi](#verifikasi-dengan-contoh-materi)
9. [Contoh Keluaran](#contoh-keluaran)
10. [Batasan dan Catatan Keamanan](#batasan-dan-catatan-keamanan)
11. [Pemecahan Masalah](#pemecahan-masalah)

---

## Studi Kasus

Bob ingin mengirim pesan rahasia kepada Alice lewat saluran yang tidak aman, sehingga penyadap bisa membaca semua yang lewat. Programnya berjalan dalam lima tahap:

| Tahap | Nama | Yang terjadi |
|---|---|---|
| 0 | Parameter publik | Alice dan Bob menyepakati bilangan prima `p` dan akar primitif `g`. Keduanya boleh diketahui siapa saja. |
| 1 | Diffie-Hellman | Alice dan Bob menghasilkan **kunci sesi `K` yang sama** tanpa pernah mengirim `K` itu sendiri. |
| 2 | ElGamal: kunci | Alice membuat kunci privat `x` dan kunci publik `y`. |
| 3 | ElGamal: enkripsi | Bob mengenkripsi pesan, ditambah penanda `[SESI:K]`, memakai kunci publik Alice. |
| 4 | ElGamal: dekripsi | Alice mendekripsi memakai kunci privat `x`, lalu memeriksa apakah penanda sesi cocok dengan `K` miliknya. |

Penanda sesi `[SESI:K]` ditaruh di depan pesan untuk menunjukkan bahwa dua tahap ini saling berhubungan. Kalau penanda hasil dekripsi tidak cocok dengan `K` hasil Diffie-Hellman, pesan ditolak.

---

## Isi Repositori

| File | Fungsi |
|---|---|
| `diffie_hellman_elgamal.py` | Program utama versi Python (menu di terminal). |
| `dh_elgamal.html` | Versi web. Berdiri sendiri, tinggal dibuka di browser. |
| `jalankan_web.py` | Peluncur kecil untuk membuka versi web lewat server lokal. |
| `Laporan_Program_DH_ElGamal.docx` | Laporan program. |
| `README.md` | Dokumen ini. |

---

## Cara Menjalankan

### Prasyarat

- Python 3 untuk versi Python dan peluncur (cek dengan `python --version`).
- Browser modern (Chrome, Edge, atau Firefox) untuk versi web.
- Tidak ada paket tambahan. Kode Python hanya memakai modul standar `random`, `http.server`, `socketserver`, `threading`, `webbrowser`, dan `os`.

### Cara 1: versi web, klik dua kali

Buka `dh_elgamal.html` di File Explorer. File akan terbuka di browser dan langsung bisa dipakai. Tidak butuh Python dan tidak butuh internet (kalau offline, hanya jenis font yang berubah).

### Cara 2: versi web lewat Python

Taruh `jalankan_web.py` dan `dh_elgamal.html` di folder yang sama, lalu di PowerShell atau terminal:

```
python jalankan_web.py
```

Browser terbuka otomatis di `http://localhost:8000/dh_elgamal.html`. Tekan `Ctrl+C` di terminal untuk berhenti.

### Cara 3: versi Python di terminal

```
python diffie_hellman_elgamal.py
```

Menu yang muncul:

| Pilihan | Fungsi |
|---|---|
| `1` | Studi kasus dengan parameter dan kunci otomatis. Anda memilih ukuran bit `p` (default 64, minimal 16) dan pesan. |
| `2` | Studi kasus manual. Anda memasukkan `p`, `g`, kunci privat, dan pesan sendiri. |
| `3` | Verifikasi dengan contoh angka dari materi kuliah. |
| `0` | Keluar. |

Di Windows, jika `python` tidak dikenali, coba `py` sebagai gantinya. Di Mac atau Linux, gunakan `python3`.

### Memakai versi web

1. Isi **nama kelompok** dan **nama anggota** di bagian atas halaman.
2. Pada tab **Studi kasus**, pilih ukuran bit `p` dan tulis pesan Bob.
3. Kolom `p`, `g`, `x`, `y`, dan kunci ElGamal bersifat opsional. Kosongkan untuk nilai acak, isi untuk memakai nilai sendiri.
4. Klik **Jalankan studi kasus**. Buka panel **Rumus & penjelasan** di tiap tahap untuk melihat perhitungannya.
5. Tab **Bedah rumus** berisi ringkasan teori. Tab **Uji contoh angka** membandingkan hasil dengan contoh materi.
6. Tombol **Simpan sebagai PDF** membuka dialog cetak browser. Pilih "Save as PDF".

---

## Alur Program

```
          Alice                                        Bob
            |                                           |
   TAHAP 0  |<------ sepakat p dan g (publik) --------->|
            |                                           |
   TAHAP 1  |  pilih x (rahasia)        pilih y (rahasia)|
            |  X = g^x mod p                Y = g^y mod p|
            |-------------- X ------------------------->|
            |<------------- Y --------------------------|
            |  K  = Y^x mod p            K' = X^y mod p |
            |          K = K'  (kunci sesi sama)        |
            |                                           |
   TAHAP 2  |  privat x', publik y' = g^x' mod p        |
            |-------------- (y', g, p) ---------------->|
            |                                           |
   TAHAP 3  |        payload = "[SESI:K] " + pesan      |
            |        tiap blok m -> (a, b)              |
            |<------------- cipherteks (a, b) ----------|
            |                                           |
   TAHAP 4  |  m = b * (a^x')^-1 mod p                  |
            |  cek penanda [SESI:K] cocok atau tidak    |
```

---

## Rumus yang Dipakai

### Diffie-Hellman

| Langkah | Rumus |
|---|---|
| Publik Alice | `X = g^x mod p` |
| Publik Bob | `Y = g^y mod p` |
| Kunci sesi Alice | `K = Y^x mod p` |
| Kunci sesi Bob | `K' = X^y mod p` |

Mengapa `K = K'`:

```
K  = Y^x = (g^y)^x = g^(xy) mod p
K' = X^y = (g^x)^y = g^(xy) mod p
```

Penyadap hanya mengetahui `p`, `g`, `X`, dan `Y`. Untuk mendapatkan `K`, ia harus mencari `x` atau `y` dari `X` atau `Y`. Ini disebut **masalah logaritma diskrit**, yang sulit dihitung untuk bilangan besar.

### ElGamal

| Langkah | Rumus |
|---|---|
| Kunci privat | `x`, dengan `1 < x < p-1` |
| Kunci publik | `y = g^x mod p`, dibagikan sebagai `(y, g, p)` |
| Enkripsi | `a = g^k mod p` dan `b = y^k * m mod p` |
| Cipherteks | `(a, b)` untuk setiap blok |
| Dekripsi | `m = b * (a^x)^-1 mod p` |

`k` adalah bilangan acak yang dibuat baru untuk setiap blok, dan `m` harus memenuhi `0 <= m < p`.

Mengapa dekripsi benar:

```
a^x = g^(kx) mod p
b   = y^k * m = g^(xk) * m mod p
b * (a^x)^-1 = g^(xk) * m * g^(-kx) = m mod p
```

Invers `(a^x)^-1` dihitung dengan teorema Fermat kecil:

```
(a^x)^-1 = a^(p-1-x) mod p
```

### Perhitungan pendukung

| Perhitungan | Metode |
|---|---|
| `basis^eksp mod m` | Square-and-multiply (perpangkatan cepat) |
| Invers modulo | Extended Euclid |
| Uji bilangan prima | Miller-Rabin |
| Pembangkit `p` | Prima aman: `p = 2q + 1` dengan `q` prima |
| Akar primitif `g` | `g^((p-1)/q) mod p != 1` untuk setiap faktor prima `q` dari `p-1` |

Pada prima aman, faktor prima `p-1` hanya `{2, q}`, jadi pengecekan akar primitif cukup dua perpangkatan.

---

## Penjelasan Fungsi pada Kode Python

### Matematika dasar

| Fungsi | Kegunaan |
|---|---|
| `modpow(basis, eksp, mod)` | Menghitung `basis^eksp mod mod` dengan square-and-multiply. Pengganti `pow(a, b, m)` bawaan Python. |
| `egcd(a, b)` | Extended Euclid. Mengembalikan `(g, s, t)` dengan `a*s + b*t = fpb(a, b)`. |
| `modinv(a, mod)` | Invers `a` terhadap modulo `mod`. Menghasilkan galat jika tidak ada. |
| `is_prima(n)` | Uji keprimaan Miller-Rabin. |
| `faktor_prima(n)` | Faktor prima unik dari `n` dengan trial division (untuk `n` kecil sampai menengah). |
| `is_akar_primitif(g, p, faktor)` | Memeriksa apakah `g` akar primitif dari `p`. |
| `cari_akar_primitif(p, faktor)` | Mencari `g` terkecil yang menjadi akar primitif. |
| `bangkitkan_parameter(bits)` | Membangkitkan prima aman `p` dan akar primitif `g`. |

### Diffie-Hellman

| Fungsi | Kegunaan |
|---|---|
| `dh_publik(g, privat, p)` | Menghitung nilai publik `g^privat mod p`. |
| `dh_kunci_sesi(publik_lawan, privat_sendiri, p)` | Menghitung kunci sesi. |

### ElGamal

| Fungsi | Kegunaan |
|---|---|
| `eg_bangkitkan_kunci(p, g, x)` | Membuat pasangan kunci `(x, y)`. |
| `eg_enkripsi_blok(m, y, g, p, k)` | Mengenkripsi satu blok menjadi `(a, b)`. |
| `eg_dekripsi_blok(a, b, x, p)` | Mendekripsi satu blok. |
| `panjang_blok(p)` | Menentukan jumlah digit per blok. |
| `teks_ke_blok(teks, p)` | Mengubah teks menjadi daftar blok angka. |
| `blok_ke_teks(blok, p)` | Mengubah blok angka kembali menjadi teks. |

### Studi kasus dan menu

| Fungsi | Kegunaan |
|---|---|
| `studi_kasus(p, g, pesan, ...)` | Menjalankan tahap 0 sampai 4 dan mencetak semua nilai antara. |
| `contoh_slide()` | Menjalankan contoh angka dari materi untuk membuktikan implementasi benar. |
| `mode_otomatis()` | Menu 1: parameter dan kunci otomatis. |
| `mode_manual()` | Menu 2: parameter dan kunci dimasukkan sendiri. |
| `main()` | Menu utama. |

Versi web memakai nama fungsi yang hampir sama (`modpow`, `egcd`, `modinv`, `isPrima`, `bangkit`, `egEnk`, `egDek`, `teksBlok`, `blokTeks`), ditulis dalam JavaScript dengan tipe `BigInt` supaya bilangan besar tetap tepat.

---

## Cara Teks Diubah Menjadi Angka

ElGamal bekerja pada bilangan, bukan teks, sehingga pesan diubah dulu:

1. Setiap karakter diubah menjadi **3 digit** kode ASCII. Contoh: `A` menjadi `065`. Karakter dengan kode 1000 atau lebih diganti `?`.
2. Semua digit digabung, lalu dipotong menjadi blok.
3. Panjang blok adalah **kelipatan 3 terbesar yang lebih kecil dari jumlah digit `p`**, supaya nilai blok selalu lebih kecil dari `p`.
4. Jika digit terakhir kurang, diisi angka `0` (setara karakter NUL). Karakter ini dibuang saat dekripsi.

Karena itu `p` minimal harus 4 digit supaya satu blok bisa memuat satu karakter. Di mode manual, `p` minimal 1000.

---

## Verifikasi dengan Contoh Materi

Menu `3` pada Python dan tab **Uji contoh angka** pada web menjalankan dua contoh dari materi kuliah. Hasil yang diharapkan:

**Diffie-Hellman** dengan `n = 251`, `g = 6`, `x = 124`, `y = 158`:

| Nilai | Hasil |
|---|---|
| `X = 6^124 mod 251` | 209 |
| `Y = 6^158 mod 251` | 197 |
| `K = K'` | 79 |

**ElGamal** dengan `p = 2273`, `g = 3`, `x = 243`, plainteks `HALO` (A=00 sampai Z=25):

| Nilai | Hasil |
|---|---|
| Kunci publik `y` | 461 |
| Blok plainteks | 0700 dan 1114 |
| `c1` (dengan `k = 1463`) | (1439, 74) |
| `c2` (dengan `k = 2001`) | (1220, 1682) |
| Hasil dekripsi | HALO |

Jika semua nilai cocok, programnya menampilkan keterangan **SESUAI**.

---

## Contoh Keluaran

Potongan keluaran versi Python untuk `p` kecil (nilai Anda akan berbeda karena kunci dipilih acak):

```
TAHAP 1 - DIFFIE-HELLMAN : kesepakatan kunci sesi
  Alice memilih x (RAHASIA)      = ...
  Alice mengirim X = g^x mod p   = ...
  Bob   memilih y (RAHASIA)      = ...
  Bob   mengirim Y = g^y mod p   = ...
  Alice menghitung K  = Y^x mod p = ...
  Bob   menghitung K' = X^y mod p = ...
  K == K' ?  YA, kunci sesi sama

TAHAP 4 - ELGAMAL : Alice mendekripsi dengan kunci privat x
  Payload hasil dekripsi : [SESI:...] Halo Alice, nilai ETS Kriptografi kita A!
  Verifikasi penanda sesi : COCOK dengan kunci sesi Diffie-Hellman Alice
  PESAN ASLI              : Halo Alice, nilai ETS Kriptografi kita A!
```

---

## Batasan dan Catatan Keamanan

Program ini dibuat untuk **pembelajaran**, bukan untuk melindungi data sungguhan.

- Ukuran `p` di program (16 sampai 64 bit) **jauh terlalu kecil** untuk keamanan nyata. Pada praktiknya dipakai `p` minimal 2048 bit.
- Diffie-Hellman versi dasar **tidak mengotentikasi** kedua pihak, sehingga rentan terhadap serangan man-in-the-middle.
- Penanda `[SESI:K]` hanya untuk mendemonstrasikan keterkaitan dua tahap. Ia bukan mekanisme otentikasi yang aman.
- ElGamal di sini tidak memakai skema padding standar.
- Pencarian akar primitif lewat `faktor_prima` memakai trial division, sehingga hanya cocok untuk `p` kecil sampai menengah. Pada mode manual, pemeriksaan `g` dilewati jika `p` lebih besar dari `10^13`.
- Sumber angka acak Python adalah `random.SystemRandom`. Versi web memakai `crypto.getRandomValues` milik browser.

---

## Pemecahan Masalah

| Masalah | Penyebab dan solusi |
|---|---|
| `python` tidak dikenali di Windows | Coba `py`. Jika tetap gagal, pasang Python dari python.org dan centang "Add Python to PATH". |
| Port 8000 sudah dipakai | Ubah `PORT = 8000` di `jalankan_web.py` ke angka lain, misalnya 8080. |
| Browser tidak terbuka otomatis | Buka manual `http://localhost:8000/dh_elgamal.html`. |
| "g bukan akar primitif dari p" | Nilai `g` tidak valid untuk `p` itu. Kosongkan kolom `g` dan `p` pada web untuk memakai nilai otomatis. |
| "p harus bilangan prima >= 1000" | Pada mode manual, `p` harus prima dan minimal 1000. |
| "Kunci privat harus 1 < nilai < p-1" | Ubah nilai `x`, `y`, atau kunci ElGamal ke rentang yang benar. |
| Pembangkitan `p` 64 bit terasa lama | Wajar, karena program mencari prima aman secara acak. Pilih 32 bit untuk hasil lebih cepat. |
| `git push` ditolak (403) | Akun Anda belum punya akses tulis. Minta ditambahkan sebagai collaborator, atau fork lalu buat pull request. |
