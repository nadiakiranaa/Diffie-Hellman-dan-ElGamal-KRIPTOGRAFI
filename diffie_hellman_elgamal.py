#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STUDI KASUS : "Pengiriman Pesan Rahasia Bob -> Alice"
              memakai Diffie-Hellman (kesepakatan kunci sesi) + ElGamal (enkripsi pesan)

Tanpa library/framework kriptografi jadi. Semua operasi dibuat manual:
  - perpangkatan modulo (square-and-multiply)   -> modpow()
  - invers modulo (Extended Euclid)              -> modinv()
  - uji bilangan prima (Miller-Rabin)            -> is_prima()
  - pencarian akar primitif                      -> cari_akar_primitif()
  - Diffie-Hellman & ElGamal (kunci, enkripsi, dekripsi)
Library standar Python yang dipakai hanya `random` (sumber angka acak).

Alur studi kasus (sesuai materi Pertemuan 9):
  TAHAP 0  Alice & Bob menyepakati parameter publik  p (prima) dan g (akar primitif p)
  TAHAP 1  Diffie-Hellman      : Alice & Bob membangkitkan kunci sesi K yang SAMA
  TAHAP 2  ElGamal - Kunci     : Alice membangkitkan kunci privat x & kunci publik y
  TAHAP 3  ElGamal - Enkripsi  : Bob mengenkripsi pesan (+ penanda sesi K) dengan kunci publik Alice
  TAHAP 4  ElGamal - Dekripsi  : Alice mendekripsi dengan kunci privat x, lalu memeriksa penanda sesi K
"""

import random

_rng = random.SystemRandom()


# =====================================================================
# 1. FUNGSI MATEMATIKA DASAR (semua manual)
# =====================================================================
def modpow(basis, eksp, mod):
    """basis^eksp mod mod  (square-and-multiply), pengganti pow(a,b,m)."""
    hasil = 1
    basis %= mod
    while eksp > 0:
        if eksp & 1:
            hasil = (hasil * basis) % mod
        basis = (basis * basis) % mod
        eksp >>= 1
    return hasil


def egcd(a, b):
    """Extended Euclid: kembalikan (g, s, t) sehingga a*s + b*t = g = fpb(a,b)."""
    s0, s1, t0, t1 = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a - q * b
        s0, s1 = s1, s0 - q * s1
        t0, t1 = t1, t0 - q * t1
    return a, s0, t0


def modinv(a, mod):
    """Invers a terhadap modulo mod (a * inv = 1 mod mod)."""
    g, s, _ = egcd(a % mod, mod)
    if g != 1:
        raise ValueError("invers tidak ada")
    return s % mod


_PRIMA_KECIL = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]


def is_prima(n):
    """Uji keprimaan Miller-Rabin."""
    if n < 2:
        return False
    for p in _PRIMA_KECIL:
        if n == p:
            return True
        if n % p == 0:
            return False
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    basis = _PRIMA_KECIL[:12] + [_rng.randrange(2, n - 1) for _ in range(8)]
    for a in basis:
        x = modpow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True


def faktor_prima(n):
    """Faktor prima unik dari n (trial division, untuk n kecil/menengah)."""
    hasil, d = set(), 2
    while d * d <= n:
        while n % d == 0:
            hasil.add(d)
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        hasil.add(n)
    return hasil


def is_akar_primitif(g, p, faktor):
    """g akar primitif p  <=>  g^((p-1)/q) != 1 (mod p) untuk setiap faktor prima q dari p-1."""
    if not (1 < g < p):
        return False
    return all(modpow(g, (p - 1) // q, p) != 1 for q in faktor)


def cari_akar_primitif(p, faktor):
    g = 2
    while not is_akar_primitif(g, p, faktor):
        g += 1
    return g


def bangkitkan_parameter(bits):
    """Bangkitkan prima aman p = 2q+1 (q prima) agar akar primitif mudah dicari/diverifikasi."""
    while True:
        q = _rng.getrandbits(bits - 1) | (1 << (bits - 2)) | 1
        if is_prima(q) and is_prima(2 * q + 1):
            p = 2 * q + 1
            return p, cari_akar_primitif(p, {2, q})


# =====================================================================
# 2. DIFFIE-HELLMAN  (slide 8-11)
# =====================================================================
def dh_publik(g, privat, p):
    """X = g^x mod p  (atau Y = g^y mod p)."""
    return modpow(g, privat, p)


def dh_kunci_sesi(publik_lawan, privat_sendiri, p):
    """K = Y^x mod p (Alice)  /  K' = X^y mod p (Bob)."""
    return modpow(publik_lawan, privat_sendiri, p)


# =====================================================================
# 3. ELGAMAL  (slide 12-19)
# =====================================================================
def eg_bangkitkan_kunci(p, g, x=None):
    """Kunci privat x (1 < x < p-1), kunci publik y = g^x mod p."""
    if x is None:
        x = _rng.randrange(2, p - 1)
    return x, modpow(g, x, p)


def eg_enkripsi_blok(m, y, g, p, k=None):
    """a = g^k mod p ;  b = y^k * m mod p   -> (a, b)"""
    if not (0 <= m < p):
        raise ValueError("blok m harus pada rentang [0, p-1]")
    if k is None:
        k = _rng.randrange(2, p - 1)
    a = modpow(g, k, p)
    b = (modpow(y, k, p) * m) % p
    return a, b, k


def eg_dekripsi_blok(a, b, x, p):
    """m = b * (a^x)^-1 mod p, dengan (a^x)^-1 = a^(p-1-x) mod p."""
    inv = modpow(a, p - 1 - x, p)
    return (b * inv) % p, inv


# ---- pengubah teks <-> blok bilangan ---------------------------------
def panjang_blok(p):
    """Jumlah digit per blok (kelipatan 3, karena 1 karakter = 3 digit kode ASCII)."""
    d = ((len(str(p)) - 1) // 3) * 3
    if d < 3:
        raise ValueError("p terlalu kecil (minimal 4 digit) untuk mengkode teks")
    return d


def teks_ke_blok(teks, p):
    d = panjang_blok(p)
    digit = "".join("%03d" % (ord(c) if ord(c) < 1000 else ord("?")) for c in teks)
    while len(digit) % d:
        digit += "0"                       # padding -> karakter NUL, dibuang saat dekripsi
    return [int(digit[i:i + d]) for i in range(0, len(digit), d)]


def blok_ke_teks(blok, p):
    d = panjang_blok(p)
    digit = "".join(str(m).zfill(d) for m in blok)
    teks = "".join(chr(int(digit[i:i + 3])) for i in range(0, len(digit), 3))
    return teks.rstrip("\x00")


# =====================================================================
# 4. STUDI KASUS LENGKAP
# =====================================================================
def garis(judul=""):
    print("\n" + "=" * 70)
    if judul:
        print(judul)
        print("=" * 70)


def studi_kasus(p, g, pesan, x_dh=None, y_dh=None, x_eg=None):
    """Menjalankan TAHAP 0-4 dan mencetak semua nilai antara."""
    garis("TAHAP 0 - PARAMETER PUBLIK (disepakati Alice & Bob, boleh diketahui penyadap)")
    print(f"  p (bilangan prima)       = {p}")
    print(f"  g (akar primitif dari p) = {g}")
    print(f"  jumlah bit p             = {p.bit_length()}")

    # ---------------- TAHAP 1: Diffie-Hellman ----------------
    garis("TAHAP 1 - DIFFIE-HELLMAN : kesepakatan kunci sesi")
    if x_dh is None:
        x_dh = _rng.randrange(2, p - 1)
    if y_dh is None:
        y_dh = _rng.randrange(2, p - 1)
    X = dh_publik(g, x_dh, p)
    Y = dh_publik(g, y_dh, p)
    print(f"  Alice memilih x (RAHASIA)      = {x_dh}")
    print(f"  Alice mengirim X = g^x mod p   = {X}")
    print(f"  Bob   memilih y (RAHASIA)      = {y_dh}")
    print(f"  Bob   mengirim Y = g^y mod p   = {Y}")
    K = dh_kunci_sesi(Y, x_dh, p)
    K2 = dh_kunci_sesi(X, y_dh, p)
    print(f"  Alice menghitung K  = Y^x mod p = {K}")
    print(f"  Bob   menghitung K' = X^y mod p = {K2}")
    print(f"  K == K' ?  {'YA, kunci sesi sama' if K == K2 else 'TIDAK (ada kesalahan)'}")
    print(f"  Penyadap hanya tahu p, g, X, Y -> sulit mencari K (masalah logaritma diskrit)")
    if K != K2:
        raise SystemExit("Diffie-Hellman gagal.")

    # ---------------- TAHAP 2: ElGamal - kunci ----------------
    garis("TAHAP 2 - ELGAMAL : pembangkitan kunci Alice")
    x_eg, y_eg = eg_bangkitkan_kunci(p, g, x_eg)
    print(f"  Kunci privat Alice  x           = {x_eg}   (RAHASIA)")
    print(f"  Kunci publik Alice  y = g^x mod p = {y_eg}")
    print(f"  Kunci publik        (y, g, p)   = ({y_eg}, {g}, {p})")

    # ---------------- TAHAP 3: ElGamal - enkripsi ----------------
    garis("TAHAP 3 - ELGAMAL : Bob mengenkripsi pesan dengan kunci publik Alice")
    payload = f"[SESI:{K}] {pesan}"
    print(f"  Pesan asli              : {pesan}")
    print(f"  Payload (+ penanda sesi): {payload}")
    blok = teks_ke_blok(payload, p)
    print(f"  Panjang blok            : {panjang_blok(p)} digit  ->  {len(blok)} blok")
    print(f"  Blok plainteks m_i      : {blok}")
    cipher = []
    for i, m in enumerate(blok, 1):
        a, b, k = eg_enkripsi_blok(m, y_eg, g, p)
        cipher.append((a, b))
        print(f"  Blok {i}: m={m}")
        print(f"          k (acak)      = {k}")
        print(f"          a = g^k mod p = {a}")
        print(f"          b = y^k*m mod p = {b}")
        print(f"          cipherteks c{i} = (a, b) = ({a}, {b})")
    print("\n  Cipherteks yang dikirim ke Alice (lewat saluran tidak aman):")
    print("   ", cipher)

    # ---------------- TAHAP 4: ElGamal - dekripsi ----------------
    garis("TAHAP 4 - ELGAMAL : Alice mendekripsi dengan kunci privat x")
    hasil = []
    for i, (a, b) in enumerate(cipher, 1):
        m, inv = eg_dekripsi_blok(a, b, x_eg, p)
        hasil.append(m)
        print(f"  Blok {i}: (a^x)^-1 = a^(p-1-x) mod p = {inv}")
        print(f"          m = b * (a^x)^-1 mod p       = {m}")
    plain = blok_ke_teks(hasil, p)
    print(f"\n  Payload hasil dekripsi : {plain}")
    tag = f"[SESI:{K}] "
    if plain.startswith(tag):
        print(f"  Verifikasi penanda sesi : COCOK dengan kunci sesi Diffie-Hellman Alice (K = {K})")
        print(f"  PESAN ASLI              : {plain[len(tag):]}")
    else:
        print("  Verifikasi penanda sesi : TIDAK COCOK -> pesan ditolak!")
    garis()


# =====================================================================
# 5. REPLIKASI CONTOH SLIDE (untuk membuktikan implementasi benar)
# =====================================================================
def contoh_slide():
    garis("CONTOH SLIDE 11 - Diffie-Hellman  (n=251, g=6, x=124, y=158)")
    n, g, x, y = 251, 6, 124, 158
    X, Y = dh_publik(g, x, n), dh_publik(g, y, n)
    K, K2 = dh_kunci_sesi(Y, x, n), dh_kunci_sesi(X, y, n)
    print(f"  X = 6^124 mod 251 = {X}  (slide: 209)")
    print(f"  Y = 6^158 mod 251 = {Y}  (slide: 197)")
    print(f"  K = {K}, K' = {K2}      (slide: 79)")
    print("  HASIL:", "SESUAI SLIDE" if (X, Y, K, K2) == (209, 197, 79, 79) else "BERBEDA")

    garis("CONTOH SLIDE 14-19 - ElGamal  (p=2273, g=3, x=243, plainteks 'HALO')")
    p, g, x = 2273, 3, 243
    _, yk = eg_bangkitkan_kunci(p, g, x)
    print(f"  Kunci publik y = 3^243 mod 2273 = {yk}  (slide: 461)")
    teks = "HALO"
    m_all = "".join("%02d" % (ord(c) - ord("A")) for c in teks)       # A=00 ... Z=25
    blok = [int(m_all[i:i + 4]) for i in range(0, len(m_all), 4)]
    print(f"  m = {m_all} -> blok {blok}  (slide: 0700 dan 1114)")
    ks = [1463, 2001]
    cip = []
    for m, k in zip(blok, ks):
        a, b, _ = eg_enkripsi_blok(m, yk, g, p, k)
        cip.append((a, b))
        print(f"  Enkripsi m={m}, k={k} -> (a,b) = ({a}, {b})")
    print("  Slide: c1=(1439,74), c2=(1220,1682) ->",
          "SESUAI" if cip == [(1439, 74), (1220, 1682)] else "BERBEDA")
    hasil = [eg_dekripsi_blok(a, b, x, p)[0] for a, b in cip]
    digit = "".join("%04d" % m for m in hasil)
    teks2 = "".join(chr(int(digit[i:i + 2]) + 65) for i in range(0, len(digit), 2))
    print(f"  Dekripsi -> blok {hasil} -> '{teks2}'  (slide: HALO)")
    garis()


# =====================================================================
# 6. MENU
# =====================================================================
def baca_int(prompt):
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("  Masukkan bilangan bulat.")


def mode_otomatis():
    s = input("Ukuran bit p [default 64, min 16]: ").strip()
    bits = int(s) if s.isdigit() and int(s) >= 16 else 64
    pesan = input("Pesan rahasia Bob untuk Alice [Enter = contoh]: ").strip()
    if not pesan:
        pesan = "Halo Alice, nilai ETS Kriptografi kita A!"
    print("\nMembangkitkan p (prima aman) dan g (akar primitif)...")
    p, g = bangkitkan_parameter(bits)
    studi_kasus(p, g, pesan)


def mode_manual():
    p = baca_int("p (bilangan prima, >= 1000): ")
    if p < 1000 or not is_prima(p):
        print("  p harus bilangan prima >= 1000.")
        return
    g = baca_int("g (akar primitif dari p): ")
    if p <= 10 ** 13:
        if not is_akar_primitif(g, p, faktor_prima(p - 1)):
            print("  g bukan akar primitif dari p.")
            return
    else:
        print("  (p besar, pemeriksaan akar primitif dilewati)")
    x = baca_int("Kunci privat DH Alice x [1 < x < p-1]: ")
    y = baca_int("Kunci privat DH Bob   y [1 < y < p-1]: ")
    xe = baca_int("Kunci privat ElGamal Alice [1 < x < p-1]: ")
    if not all(1 < v < p - 1 for v in (x, y, xe)):
        print("  Kunci privat harus 1 < nilai < p-1.")
        return
    pesan = input("Pesan: ")
    studi_kasus(p, g, pesan, x, y, xe)


def main():
    while True:
        print("\n=== DIFFIE-HELLMAN + ELGAMAL (tanpa library kriptografi) ===")
        print("1. Studi kasus (parameter & kunci otomatis)")
        print("2. Studi kasus (parameter & kunci manual)")
        print("3. Verifikasi dengan contoh angka di slide")
        print("0. Keluar")
        pil = input("Pilih: ").strip()
        if pil == "1":
            mode_otomatis()
        elif pil == "2":
            mode_manual()
        elif pil == "3":
            contoh_slide()
        elif pil == "0":
            break


if __name__ == "__main__":
    main()
