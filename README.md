<div align="center">

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        🔑  T O P N O D   A U T O   B O T  🔑                ║
║                                                              ║
║         Single Device · Auto Wallet · Seed Phrase           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/VSPhone-Cloud_Device-FF6B00?style=for-the-badge)](https://vsphone.com)
[![Mode](https://img.shields.io/badge/Mode-Single_Device-brightgreen?style=for-the-badge)]()

</div>

---

## ⚡ Quick Start

```bash
# 1. Install dependency
pip install -r requirements.txt

# 2. Jalankan bot
python topnod.py
```

---

## ⚙️ Konfigurasi Awal

Buka `topnod.py`, edit bagian **KONFIGURASI** di baris paling atas:

```python
EMAIL         = "email_vsphone@gmail.com"
PASSWORD_MD5  = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # hash MD5 dari password VSPhone
PAD_CODE      = "PADCODE_DEVICE_KAMU"              # padCode device target
DEVICE_NAME   = "Nama Device"

REFERRAL_CODE   = "KODEREF"     # referral code default
WALLET_PASSWORD = "password123" # password wallet yang akan dibuat
OTP_TIMEOUT     = 180           # maks detik tunggu OTP (default 3 menit)
```

> 💡 **Cara dapat PASSWORD_MD5:**
> ```bash
> echo -n "passwordkamu" | md5sum
> ```
> Salin hasilnya (tanpa tanda `-` di akhir).

> 💡 **Cara dapat PAD_CODE:**
> Buka VSPhone → klik device → lihat URL atau info device, salin kode seperti `ACP250929NBUC1VX`.

---

## 🚀 Alur Jalannya Script

```
python topnod.py
       │
       ├─ [1] Input referral code
       ├─ [2] Pilih APK TopNod
       │
       ├─ Install APK ke device
       ├─ Launch TopNod
       ├─ Set resolusi 1080×1920
       │
       ├─ Buat email temporer (mail.tm)
       ├─ Navigasi → form email → kirim OTP
       │
       ├─ ⚠️  CAPTCHA MANUAL → tekan Enter
       │
       ├─ Polling OTP otomatis
       ├─ Input OTP + referral + password
       ├─ Handle popup biometric
       │
       ├─ ✔  Wallet berhasil → simpan ke wallet_sukses.txt
       │
       └─ Get Seed Phrase
            ├─ Navigasi ke Show Recovery Phrase
            ├─ Polling OTP seed phrase
            └─ Input OTP → Confirm
```

---

## 📋 Panduan Lengkap

### `[1]` Referral Code

```
  Referral code saat ini: ISIREF
  Masukkan referral baru (kosong = pakai default): █
```

Ketik referral code baru lalu Enter, atau langsung Enter untuk pakai default.

---

### `[2]` Pilih APK

```
  ✘  Tidak ada APK bernama topnod. APK tersedia (2):
    1.  topnod_v1.3.5.apk  (45.2 MB)  id=1001
    2.  topnod_v1.3.4.apk  (44.8 MB)  id=1000

  Pilih nomor APK (1-2): █
```

Jika hanya 1 APK bernama `topnod`, langkah ini dilewati otomatis.

---

### `[3]` Selesaikan CAPTCHA

```
  ⚠   Buka VSPhone, verifikasi CAPTCHA di device,
      lalu tekan ENTER untuk lanjut.

    → Tekan ENTER setelah captcha selesai...  █
```

Buka VSPhone → masuk ke device → selesaikan captcha → kembali ke terminal → Enter.

---

### `[4]` OTP Tidak Masuk? Bisa Kirim Ulang

```
  ✘  OTP tidak masuk dalam 180s

  Kirim ulang OTP? (y = kirim ulang / n = skip): █
```

Ketik `y` untuk kirim ulang OTP (captcha akan muncul lagi).
Ketik `n` untuk skip dan hentikan proses.

---

### `[5]` Seed Phrase Otomatis

Setelah wallet berhasil dibuat, script otomatis mengambil seed phrase:

- Navigasi ke **Settings → Show Recovery Phrase**
- Kirim dan polling OTP secara otomatis
- Input OTP → Confirm

> ⚠️ Seed phrase tampil di layar device setelah OTP berhasil diinput. Baca dan simpan secara manual dari VSPhone.

---

### Hentikan Script

Tekan `Ctrl + C` kapan saja:

```
╔══════════════════ Script Dihentikan ══════════════════╗
║  Script dihentikan manual (Ctrl+C)                   ║
╚═══════════════════════════════════════════════════════╝
```

---

## 📁 Output

| File | Keterangan |
|------|------------|
| `wallet_sukses.txt` | Hasil wallet: Device, Email, Password, Referral |
| `device_PADCODE_log_*.txt` | Log lengkap semua aktivitas — simpan 5 file terakhir |

**Contoh `wallet_sukses.txt`:**
```
Device=ACP250929NBUC1VX | Email=abc123@mail.tm | Pass=masuk123 | Ref=REFCODE
```

---

## ⚠️ Catatan

- Jangan tutup terminal selama script berjalan
- Pastikan APK TopNod sudah diupload ke cloud storage VSPhone
- Koordinat dikalibrasi untuk resolusi **1080×1920 DPI 320** — jangan ubah resolusi secara manual
- Gunakan Python **3.10+** (diperlukan untuk `str | None` type hint)

---
<br><br>

<div align="center">

---

<img src="photo_2026-03-10_01-33-02.jpg" width="140" alt="Silent Private Community"/>

<br>

```
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░                                                    ░
░        S P E C I A L   T H A N K S               ░
░                                                    ░
░              to the one who started it            ░
░                                                    ░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
```

### `Mr. Silent`
#### *Founder · Silent Private Community*

<br>

> *Di balik layar, ada seseorang yang tidak butuh sorotan —*
> *cukup hasilnya yang berbicara.*
> *Terima kasih sudah berbagi tanpa pamrih.*

<br>

Tools ini tidak akan pernah exist tanpa kepercayaan,
ilmu, dan ekosistem yang sudah **Mr. Silent** bangun
di dalam **Silent Private Community**.

Setiap baris kode di sini adalah bentuk terima kasih
yang ditulis dalam bahasa Python. 🐍🔑

<br>

```
  ███████╗██╗██╗     ███████╗███╗   ██╗████████╗
  ██╔════╝██║██║     ██╔════╝████╗  ██║╚══██╔══╝
  ███████╗██║██║     █████╗  ██╔██╗ ██║   ██║
  ╚════██║██║██║     ██╔══╝  ██║╚██╗██║   ██║
  ███████║██║███████╗███████╗██║ ╚████║   ██║
  ╚══════╝╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝
  P R I V A T E   C O M M U N I T Y  🔑
```

<br>

**Move in silence. Strike with precision.**

<br>

---

*© Silent Private Community · All rights reserved*

</div>
