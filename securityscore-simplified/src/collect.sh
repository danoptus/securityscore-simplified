#!/bin/bash

DOMAIN=$(grep "domain" src/config.yaml | cut -d' ' -f2)
OUTPUT_DIR="reports"

mkdir -p $OUTPUT_DIR

echo "[+] Enumerando subdomínios..."
amass enum -d $DOMAIN -o $OUTPUT_DIR/subdomains.txt

echo "[+] Procurando leaks no GitHub..."
trufflehog https://github.com/ $DOMAIN --json > $OUTPUT_DIR/github_leaks.json

echo "[+] Escaneando vulnerabilidades..."
nuclei -u https://$DOMAIN -u https://www.$DOMAIN -o $OUTPUT_DIR/vulnerabilities.txt

echo "[+] Verificando certificados..."
nmap --script ssl-enum-ciphers -p 443 $DOMAIN > $OUTPUT_DIR/sslcheck.txt

echo "[+] Verificação de email"
dig TXT _dmarc.$DOMAIN > $OUTPUT_DIR/dmarc_check.txt
dig TXT $DOMAIN > $OUTPUT_DIR/spf_check.txt

echo "[+] Coleta concluída!"
