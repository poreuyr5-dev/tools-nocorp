# NANOZ CORP - Termux System & File Tools (Python3 Edition)

Toolkit Termux berbasis Python3 berisi 48 fitur legal untuk maintenance sistem
dan manajemen file. Tidak ada fitur untuk hacking, serangan jaringan, atau
pelanggaran privasi.

## Fitur
- **System Tools (20 fitur):** info device/CPU/RAM/storage/baterai, update & install paket, bersihkan cache, cek IP publik, manajemen proses, dll.
- **File Tools (28 fitur):** compress/extract, bulk rename, backup/restore, cari file, hitung checksum SHA256, split/join file, tree folder, dll.

## Cara Install di Termux

```bash
pkg install -y git python
git clone https://github.com/poreuyr5-dev/tools-nocorp.git
cd tools-nocorp
bash install.sh
```

Setelah itu jalankan kapan saja dengan:

```bash
nanoz
```

Atau langsung tanpa install command shortcut:

```bash
python3 nanoz.py
```

## Cara Upload Script Ini ke GitHub Kamu Sendiri

1. Buat repo baru di GitHub, misal `nanoz-termux-tools-py`.
2. Di Termux/komputer, masuk ke folder project ini lalu jalankan:

```bash
git init
git add .
git commit -m "Initial commit - NanoZ Corp Termux Tools (Python3)"
git branch -M main
git remote add origin https://github.com/USERNAME/nanoz-termux-tools-py.git
git push -u origin main
```

3. Ganti `USERNAME` dengan username GitHub kamu.
4. Kalau diminta login, pakai Personal Access Token GitHub (bukan password biasa).

## Struktur Project

```
nanoz-termux-tools-py/
├── nanoz.py       # Script utama (menu + semua fitur, pure Python3)
├── install.sh     # Installer, bikin command "nanoz"
└── README.md      # Panduan ini
```

## Catatan
- Butuh `python3` (otomatis diinstall oleh `install.sh`).
- Beberapa fitur (info baterai, text-to-speech) butuh app **Termux:API** dari F-Droid/Play Store plus paket `termux-api`.
- Semua fitur hanya beroperasi pada file/perangkat milik sendiri.
