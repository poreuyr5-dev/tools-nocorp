#!/data/data/com.termux/files/usr/bin/bash
# Installer NanoZ Corp Termux Tools (Python3 Edition)
echo "Menyiapkan NanoZ Corp Termux Tools (Python3)..."

pkg update -y
pkg install -y git python

chmod +x nanoz.py

BIN_DIR="$PREFIX/bin"
INSTALL_DIR="$(pwd)"
cat > "$BIN_DIR/nanoz" << EOF
#!/data/data/com.termux/files/usr/bin/bash
python3 "$INSTALL_DIR/nanoz.py"
EOF
chmod +x "$BIN_DIR/nanoz"

echo ""
echo "Instalasi selesai!"
echo "Jalankan toolkit dengan mengetik: nanoz"
