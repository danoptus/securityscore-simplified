import json
import smtplib
import requests
import os

def send_email(subject, body):
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    receiver = os.getenv("EMAIL_RECEIVER")

    if not all([sender, password, receiver]):
        print("[!] Email desativado (credenciais não configuradas)")
        return

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        msg = f"Subject: {subject}\n\n{body}"
        server.sendmail(sender, receiver, msg)
        server.quit()
        print("[+] Email enviado!")
    except Exception as e:
        print(f"[!] Erro ao enviar e-mail: {e}")

def send_slack(message):
    webhook = os.getenv("SLACK_WEBHOOK")
    if not webhook:
        return
    requests.post(webhook, json={"text": message})
    print("[+] Mensagem enviada ao Slack!")

def send_google_chat(message):
    webhook = os.getenv("GOOGLE_CHAT_WEBHOOK")
    if not webhook:
        return
    requests.post(webhook, json={"text": message})
    print("[+] Mensagem enviada ao Google Chat!")

def check_and_notify():
    try:
        with open("reports/latest.json") as f:
            result = json.load(f)
    except Exception as e:
        print(f"[!] Não foi possível carregar resultados: {e}")
        return

    if result["score"] < 5:
        msg = f"""
🚨 ALTA AMEAÇA DETECTADA!
Score atual: {result["score"]}
Detalhes: {result["details"]}
        """
        send_email("🚨 SecurityScore abaixo de 5!", msg)
        send_slack(msg)
        send_google_chat(msg)

if __name__ == "__main__":
    check_and_notify()
