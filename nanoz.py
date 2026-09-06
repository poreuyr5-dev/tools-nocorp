#!/usr/bin/env python3
# ============================================================
#  NANOZ CORP - Termux System & File Tools (Python3 Edition)
#  48 Fitur Legal untuk maintenance perangkat & manajemen file
#  Tidak ada fitur untuk hacking/serangan/pelanggaran privasi
# ============================================================

import os
import sys
import shutil
import subprocess
import hashlib
import tarfile
import zipfile
from pathlib import Path
from datetime import datetime, timedelta

RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
CYAN = "\033[1;36m"
NC = "\033[0m"

HOME = str(Path.home())
BACKUP_DIR = os.path.join(HOME, "nanoz_backup")
os.makedirs(BACKUP_DIR, exist_ok=True)


def run(cmd, capture=False):
    """Jalankan perintah shell dengan aman."""
    try:
        if capture:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.stdout.strip() + result.stderr.strip()
        else:
            subprocess.run(cmd, shell=True)
    except Exception as e:
        print(f"{RED}Error: {e}{NC}")


def banner():
    os.system("clear" if os.name != "nt" else "cls")
    print(f"{RED}")
    print(r"  _   _    _    _   _  ___ ________")
    print(r" | \ | |  / \  | \ | |/ _ \__  /_  |")
    print(r" |  \| | / _ \ |  \| | | | |/ /  | |")
    print(r" | |\  |/ ___ \| |\  | |_| / /_  | |")
    print(r" |_| \_/_/   \_\_| \_|\___/____| |_|")
    print(f"{RED}          == NANOZ CORP =={NC}")
    print(f"{YELLOW}   System & File Tools - Python3 Edition{NC}\n")


def pause():
    input("\nTekan ENTER untuk kembali ke menu...")


def need_pkg(pkg):
    if shutil.which(pkg) is None:
        print(f"{YELLOW}[!] '{pkg}' belum terinstall. Menginstall...{NC}")
        run(f"pkg install -y {pkg}")


def ask(prompt, default=None):
    val = input(f"{prompt}" + (f" (default: {default}): " if default else ": "))
    return val.strip() or (default or "")


# ---------------- SYSTEM TOOLS (1-20) ----------------

def sys_device_info():
    model = run("getprop ro.product.model", capture=True) or "N/A"
    android = run("getprop ro.build.version.release", capture=True) or "N/A"
    print(f"{CYAN}Model:{NC} {model}")
    print(f"{CYAN}Android:{NC} {android}")
    print(f"{CYAN}Arch:{NC} {os.uname().machine}")


def sys_cpu_info():
    print(run("cat /proc/cpuinfo | grep -m1 'model name\\|Hardware'", capture=True))
    cores = os.cpu_count()
    print(f"Jumlah core: {cores}")


def sys_ram_info():
    out = run("free -h", capture=True)
    print(out if out else run("cat /proc/meminfo | head -5", capture=True))


def sys_storage_info():
    total, used, free = shutil.disk_usage(HOME)
    print(f"Total: {total // (2**30)} GB")
    print(f"Terpakai: {used // (2**30)} GB")
    print(f"Sisa: {free // (2**30)} GB")


def sys_battery_info():
    need_pkg("termux-api")
    out = run("termux-battery-status", capture=True)
    print(out if out else "Install app Termux:API dari F-Droid/Play Store dulu.")


def sys_uptime():
    print(run("uptime", capture=True))


def sys_public_ip():
    need_pkg("curl")
    print(run("curl -s ifconfig.me", capture=True))


def sys_update_upgrade():
    run("pkg update -y && pkg upgrade -y")


def sys_install_common():
    run("pkg install -y curl wget git python nodejs vim nano zip unzip")


def sys_clean_cache():
    run("pkg clean")
    prefix = os.environ.get("PREFIX", "")
    if prefix:
        run(f"rm -rf {prefix}/tmp/*")
    print("Cache dibersihkan.")


def sys_termux_version():
    out = run("termux-info", capture=True)
    print(out[:800] if out else "termux-info tidak tersedia.")


def sys_shell_info():
    print(f"Shell: {os.environ.get('SHELL', 'N/A')}")
    print(f"Python: {sys.version}")


def sys_setup_storage():
    run("termux-setup-storage")


def sys_process_list():
    print(run("top -n 1 | head -20", capture=True))


def sys_kill_process():
    name = ask("Nama proses yang mau di-kill")
    result = run(f"pkill -f '{name}'", capture=True)
    print(f"Proses '{name}' dihentikan." if result == "" else result)


def sys_restart_shell():
    print("Merestart shell...")
    os.execvp(os.environ.get("SHELL", "bash"), [os.environ.get("SHELL", "bash")])


def sys_ping_test():
    host = ask("Domain/IP untuk ping", "google.com")
    run(f"ping -c 4 {host}")


def sys_kernel_info():
    print(run("uname -a", capture=True))


def sys_check_termux_api():
    if shutil.which("termux-battery-status"):
        print("termux-api sudah ada.")
    else:
        print("Menginstall termux-api...")
        run("pkg install -y termux-api")


def sys_tts_speak():
    need_pkg("termux-api")
    text = ask("Teks untuk diucapkan")
    result = run(f"termux-tts-speak '{text}'", capture=True)
    if "not found" in result.lower():
        print("termux-api / app Termux:API belum siap.")


SYSTEM_ACTIONS = {
    "1": sys_device_info, "2": sys_cpu_info, "3": sys_ram_info, "4": sys_storage_info,
    "5": sys_battery_info, "6": sys_uptime, "7": sys_public_ip, "8": sys_update_upgrade,
    "9": sys_install_common, "10": sys_clean_cache, "11": sys_termux_version, "12": sys_shell_info,
    "13": sys_setup_storage, "14": sys_process_list, "15": sys_kill_process, "16": sys_restart_shell,
    "17": sys_ping_test, "18": sys_kernel_info, "19": sys_check_termux_api, "20": sys_tts_speak,
}


def system_menu():
    while True:
        banner()
        print(f"{GREEN}=== SYSTEM TOOLS ==={NC}")
        print(" 1) Info perangkat            11) Versi Termux")
        print(" 2) Info CPU                  12) Info shell/python")
        print(" 3) Info RAM                  13) Setup storage permission")
        print(" 4) Info storage/disk         14) List proses berjalan")
        print(" 5) Info baterai              15) Kill proses by name")
        print(" 6) Uptime                    16) Restart shell")
        print(" 7) Cek IP publik             17) Ping test")
        print(" 8) Update & upgrade pkg      18) Info kernel")
        print(" 9) Install paket umum        19) Cek/install termux-api")
        print("10) Bersihkan cache           20) Text to speech")
        print(" 0) Kembali ke menu utama\n")
        opt = ask("Pilih nomor")
        print()
        if opt == "0":
            return
        action = SYSTEM_ACTIONS.get(opt)
        if action:
            action()
        else:
            print("Pilihan tidak valid.")
        pause()


# ---------------- FILE TOOLS (1-28) ----------------

def file_list_sized():
    d = ask("Path folder", ".")
    items = []
    for p in Path(d).glob("*"):
        size = sum(f.stat().st_size for f in p.rglob("*") if f.is_file()) if p.is_dir() else p.stat().st_size
        items.append((size, p.name))
    for size, name in sorted(items, reverse=True):
        print(f"{size/1024:.1f} KB\t{name}")


def file_find_name():
    n = ask("Cari nama file")
    d = ask("Di folder", ".")
    for p in Path(d).rglob(f"*{n}*"):
        print(p)


def file_find_ext():
    e = ask("Ekstensi (misal txt)")
    d = ask("Di folder", ".")
    for p in Path(d).rglob(f"*.{e}"):
        print(p)


def file_folder_size():
    d = ask("Path folder")
    total = sum(f.stat().st_size for f in Path(d).rglob("*") if f.is_file())
    print(f"Total size: {total/1024/1024:.2f} MB")


def file_zip():
    d = ask("Folder yang mau di-zip")
    o = ask("Nama file output.zip")
    with zipfile.ZipFile(o, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in Path(d).rglob("*"):
            zf.write(f, f.relative_to(Path(d).parent))
    print(f"Selesai: {o}")


def file_unzip():
    f = ask("File zip")
    o = ask("Extract ke folder", ".")
    with zipfile.ZipFile(f, "r") as zf:
        zf.extractall(o)
    print("Selesai extract.")


def file_targz():
    d = ask("Folder yang mau di-tar.gz")
    o = ask("Nama output.tar.gz")
    with tarfile.open(o, "w:gz") as tar:
        tar.add(d, arcname=os.path.basename(d))
    print(f"Selesai: {o}")


def file_untargz():
    f = ask("File tar.gz")
    o = ask("Extract ke folder", ".")
    os.makedirs(o, exist_ok=True)
    with tarfile.open(f, "r:gz") as tar:
        tar.extractall(o)
    print("Selesai extract.")


def file_bulk_rename():
    d = ask("Folder")
    p = ask("Prefix baru")
    i = 1
    for f in sorted(Path(d).iterdir()):
        if f.is_file():
            new_name = f"{p}_{i}{f.suffix}"
            f.rename(f.parent / new_name)
            i += 1
    print("Selesai rename.")


def file_del_empty():
    d = ask("Folder")
    for f in Path(d).rglob("*"):
        if f.is_file() and f.stat().st_size == 0:
            print(f"Hapus: {f}")
            f.unlink()


def file_del_empty_dirs():
    d = ask("Folder")
    for p in sorted(Path(d).rglob("*"), reverse=True):
        if p.is_dir() and not any(p.iterdir()):
            print(f"Hapus: {p}")
            p.rmdir()


def file_backup():
    d = ask("Folder yang mau dibackup")
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = os.path.join(BACKUP_DIR, f"{os.path.basename(d.rstrip('/'))}_{ts}")
    shutil.copytree(d, dest)
    print(f"Backup tersimpan di {dest}")


def file_restore():
    print("Backup tersedia:")
    for b in os.listdir(BACKUP_DIR):
        print(f" - {b}")
    b = ask("Nama backup yang mau direstore")
    o = ask("Restore ke folder")
    shutil.copytree(os.path.join(BACKUP_DIR, b), o)
    print("Restore selesai.")


def file_project_template():
    p = ask("Nama project baru")
    for sub in ["src", "assets", "docs", "tests"]:
        os.makedirs(os.path.join(p, sub), exist_ok=True)
    Path(os.path.join(p, "README.md")).touch()
    print(f"Template project '{p}' dibuat.")


def file_chmod_helper():
    f = ask("Path file/folder")
    m = ask("Mode (misal 755)")
    run(f"chmod -R {m} '{f}'")


def file_view():
    f = ask("Path file text")
    run(f"less '{f}'")


def file_edit_nano():
    need_pkg("nano")
    f = ask("Path file")
    run(f"nano '{f}'")


def file_count_stats():
    f = ask("Path file")
    with open(f, "r", errors="ignore") as fh:
        content = fh.read()
    print(f"Baris: {content.count(chr(10))+1}  Kata: {len(content.split())}  Karakter: {len(content)}")


def file_grep_search():
    k = ask("Kata yang dicari")
    d = ask("Di folder", ".")
    for f in Path(d).rglob("*"):
        if f.is_file():
            try:
                with open(f, errors="ignore") as fh:
                    for num, line in enumerate(fh, 1):
                        if k in line:
                            print(f"{f}:{num}: {line.strip()}")
            except Exception:
                pass


def file_lowercase_names():
    d = ask("Folder")
    for f in Path(d).iterdir():
        f.rename(f.parent / f.name.lower())
    print("Selesai.")


def file_space_to_underscore():
    d = ask("Folder")
    for f in Path(d).iterdir():
        f.rename(f.parent / f.name.replace(" ", "_"))
    print("Selesai.")


def file_del_by_ext():
    d = ask("Folder")
    e = ask("Ekstensi yang mau dihapus (misal tmp)")
    for f in Path(d).rglob(f"*.{e}"):
        print(f"Hapus: {f}")
        f.unlink()


def file_move_by_ext():
    d = ask("Folder sumber")
    e = ask("Ekstensi")
    o = ask("Folder tujuan")
    os.makedirs(o, exist_ok=True)
    for f in Path(d).rglob(f"*.{e}"):
        shutil.move(str(f), o)
    print("Selesai.")


def file_checksum():
    f = ask("Path file")
    h = hashlib.sha256()
    with open(f, "rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    print(f"{h.hexdigest()}  {f}")


def file_diff():
    f1 = ask("File 1")
    f2 = ask("File 2")
    run(f"diff '{f1}' '{f2}'")


def file_split():
    f = ask("File yang mau displit")
    size_mb = float(ask("Ukuran per bagian dalam MB", "10"))
    chunk_size = int(size_mb * 1024 * 1024)
    with open(f, "rb") as infile:
        i = 0
        while True:
            chunk = infile.read(chunk_size)
            if not chunk:
                break
            with open(f"{f}_part_{i}", "wb") as outfile:
                outfile.write(chunk)
            i += 1
    print(f"Selesai split jadi {i} bagian.")


def file_join():
    prefix = ask("Prefix nama bagian (misal file.zip_part_)")
    o = ask("Nama output gabungan")
    parts = sorted(Path(".").glob(f"{prefix}*"), key=lambda p: p.name)
    with open(o, "wb") as outfile:
        for part in parts:
            with open(part, "rb") as infile:
                outfile.write(infile.read())
    print("Selesai digabung.")


def file_symlink():
    t = ask("Target asli")
    l = ask("Nama symlink")
    os.symlink(t, l)
    print("Symlink dibuat.")


def file_tree():
    d = ask("Folder", ".")

    def walk(path, prefix=""):
        entries = sorted(Path(path).iterdir())
        for i, entry in enumerate(entries):
            connector = "└── " if i == len(entries) - 1 else "├── "
            print(prefix + connector + entry.name)
            if entry.is_dir():
                extension = "    " if i == len(entries) - 1 else "│   "
                walk(entry, prefix + extension)

    walk(d)


def file_auto_delete_old():
    d = ask("Folder")
    days = int(ask("Hapus file lebih tua dari berapa hari"))
    cutoff = datetime.now() - timedelta(days=days)
    for f in Path(d).rglob("*"):
        if f.is_file() and datetime.fromtimestamp(f.stat().st_mtime) < cutoff:
            print(f"Hapus: {f}")
            f.unlink()


FILE_ACTIONS = {
    "1": file_list_sized, "2": file_find_name, "3": file_find_ext, "4": file_folder_size,
    "5": file_zip, "6": file_unzip, "7": file_targz, "8": file_untargz,
    "9": file_bulk_rename, "10": file_del_empty, "11": file_del_empty_dirs, "12": file_backup,
    "13": file_restore, "14": file_project_template, "15": file_chmod_helper, "16": file_count_stats,
    "17": file_grep_search, "18": file_lowercase_names, "19": file_space_to_underscore, "20": file_del_by_ext,
    "21": file_move_by_ext, "22": file_checksum, "23": file_diff, "24": file_split,
    "25": file_join, "26": file_symlink, "27": file_tree, "28": file_auto_delete_old,
}


def file_menu():
    while True:
        banner()
        print(f"{GREEN}=== FILE TOOLS ==={NC}")
        print(" 1) List file + size          16) Hitung baris/kata/karakter")
        print(" 2) Cari file by nama         17) Cari teks dalam file (grep)")
        print(" 3) Cari file by ekstensi     18) Ubah nama file jadi lowercase")
        print(" 4) Hitung size folder        19) Ganti spasi jadi underscore")
        print(" 5) Compress ke ZIP           20) Hapus file by ekstensi")
        print(" 6) Extract ZIP               21) Pindah file by ekstensi")
        print(" 7) Compress ke TAR.GZ        22) Buat checksum SHA256")
        print(" 8) Extract TAR.GZ            23) Bandingkan 2 file (diff)")
        print(" 9) Bulk rename file          24) Split file besar")
        print("10) Hapus file kosong         25) Gabung file hasil split")
        print("11) Hapus folder kosong       26) Buat symlink")
        print("12) Backup folder             27) Tampilkan tree folder")
        print("13) Restore backup            28) Auto delete file lama")
        print("14) Buat template project")
        print("15) Ubah permission (chmod)")
        print(" 0) Kembali ke menu utama\n")
        opt = ask("Pilih nomor")
        print()
        if opt == "0":
            return
        action = FILE_ACTIONS.get(opt)
        if action:
            try:
                action()
            except Exception as e:
                print(f"{RED}Error: {e}{NC}")
        else:
            print("Pilihan tidak valid.")
        pause()


def main_menu():
    while True:
        banner()
        print(f"{GREEN}MENU UTAMA{NC}")
        print("1) System Tools (20 fitur)")
        print("2) File Tools (28 fitur)")
        print("0) Keluar\n")
        m = ask("Pilih nomor")
        if m == "1":
            system_menu()
        elif m == "2":
            file_menu()
        elif m == "0":
            print(f"{RED}Sampai jumpa lagi - NANOZ CORP{NC}")
            sys.exit(0)
        else:
            print("Pilihan tidak valid.")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{RED}Keluar - NANOZ CORP{NC}")
        sys.exit(0)
