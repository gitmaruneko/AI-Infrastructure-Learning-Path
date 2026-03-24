"""
Notification — Teams / Email Automated Alert Script
====================================================

自動化通知腳本，支援 Microsoft Teams Webhook 與 SMTP Email 兩種通知管道。
可與日誌分析或設備監控系統整合，在偵測到異常時即時推送告警。

環境變數設定（建議使用 .env 檔或系統環境變數）：
    TEAMS_WEBHOOK_URL   — Teams Incoming Webhook URL
    SMTP_HOST           — SMTP 主機 (e.g., smtp.office365.com)
    SMTP_PORT           — SMTP 連接埠 (e.g., 587)
    SMTP_USER           — 寄件人帳號
    SMTP_PASSWORD       — 寄件人密碼
    ALERT_EMAIL_TO      — 收件人 Email（多位以逗號分隔）

使用方式：
    python notification.py --channel teams --message "High vibration detected on Unit-03"
    python notification.py --channel email --subject "ALERT" --message "Disk usage > 95%"
    python notification.py --channel both  --message "Critical: Engine RUL < 10 cycles"
"""

import argparse
import os
import smtplib
import sys
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv 未安裝時直接讀取系統環境變數


# ---------------------------------------------------------------------------
# Teams 通知 / Teams Notification
# ---------------------------------------------------------------------------


def send_teams_notification(message: str, title: str = "AI Infrastructure Alert") -> bool:
    """透過 Microsoft Teams Incoming Webhook 發送告警訊息。"""
    if not HAS_REQUESTS:
        print("[ERROR] 'requests' library is not installed. Run: pip install requests", file=sys.stderr)
        return False

    webhook_url = os.getenv("TEAMS_WEBHOOK_URL")
    if not webhook_url:
        print("[ERROR] TEAMS_WEBHOOK_URL environment variable is not set.", file=sys.stderr)
        return False

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payload = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "FF0000",
        "summary": title,
        "sections": [
            {
                "activityTitle": f"🚨 {title}",
                "activitySubtitle": f"Time: {timestamp}",
                "text": message,
                "markdown": True,
            }
        ],
    }

    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        print(f"[INFO] Teams notification sent successfully. Status: {response.status_code}")
        return True
    except requests.exceptions.RequestException as exc:
        print(f"[ERROR] Failed to send Teams notification: {exc}", file=sys.stderr)
        return False


# ---------------------------------------------------------------------------
# Email 通知 / Email Notification
# ---------------------------------------------------------------------------


def send_email_notification(
    message: str,
    subject: str = "AI Infrastructure Alert",
) -> bool:
    """透過 SMTP 發送 HTML Email 告警。"""
    smtp_host = os.getenv("SMTP_HOST", "")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER", "")
    smtp_password = os.getenv("SMTP_PASSWORD", "")
    recipients_raw = os.getenv("ALERT_EMAIL_TO", "")

    if not all([smtp_host, smtp_user, smtp_password, recipients_raw]):
        print(
            "[ERROR] Missing one or more SMTP environment variables: "
            "SMTP_HOST, SMTP_USER, SMTP_PASSWORD, ALERT_EMAIL_TO",
            file=sys.stderr,
        )
        return False

    recipients = [r.strip() for r in recipients_raw.split(",") if r.strip()]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html_body = f"""
    <html><body>
    <h2 style="color:#cc0000;">🚨 {subject}</h2>
    <p><strong>Time:</strong> {timestamp}</p>
    <hr/>
    <p>{message}</p>
    <hr/>
    <p style="color:#888;font-size:12px;">
        Sent by AI-Infrastructure-Learning-Path Notification Script
    </p>
    </body></html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"[ALERT] {subject}"
    msg["From"] = smtp_user
    msg["To"] = ", ".join(recipients)
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, recipients, msg.as_string())
        print(f"[INFO] Email sent to: {', '.join(recipients)}")
        return True
    except smtplib.SMTPException as exc:
        print(f"[ERROR] Failed to send email: {exc}", file=sys.stderr)
        return False


# ---------------------------------------------------------------------------
# CLI 入口 / Entry Point
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Teams / Email Notification Script")
    parser.add_argument(
        "--channel",
        choices=["teams", "email", "both"],
        default="teams",
        help="Notification channel",
    )
    parser.add_argument("--message", required=True, help="Alert message body")
    parser.add_argument(
        "--subject",
        default="AI Infrastructure Alert",
        help="Email subject / Teams card title",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    success = True

    if args.channel in ("teams", "both"):
        ok = send_teams_notification(args.message, title=args.subject)
        success = success and ok

    if args.channel in ("email", "both"):
        ok = send_email_notification(args.message, subject=args.subject)
        success = success and ok

    sys.exit(0 if success else 1)
