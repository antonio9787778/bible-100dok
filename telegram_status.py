import os
import pandas as pd
import requests

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

df = pd.read_csv("bible_100plan.csv")

total = int(df["read_count"].sum())
gu = int(df[df["testament"] == "구약"]["read_count"].sum())
sn = int(df[df["testament"] == "신약"]["read_count"].sum())
percent = total / 118900 * 100

message = (
    f"📖 100독 자동 리포트\n"
    f"총계: {total:,}/118,900 ({percent:.2f}%)\n"
    f"구약: {gu:,}/92,900\n"
    f"신약: {sn:,}/26,000\n\n"
    f"웹앱: https://bible-100dok-mmaymqgbirwvpfivsuwp2m.streamlit.app"
)

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
payload = {
    "chat_id": CHAT_ID,
    "text": message
}

response = requests.post(url, data=payload, timeout=30)
response.raise_for_status()

print("✅ Telegram 전송 완료!")
