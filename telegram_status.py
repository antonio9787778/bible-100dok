import pandas as pd
import requests

# GitHub Secrets 자동 로드
BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']

df = pd.read_csv('bible_100plan.csv')
total = df['read_count'].sum()
gu = df[df['testament']=='구약']['read_count'].sum()

message = f"""📖 100독 자동 리포트
총계: {total:,}/118,900 ({total/118900*100:.1f}%)
구약: {gu:,}/92,900
신약: {total-gu:,}/26,000

웹앱: https://bible-100dok-mmaymqgbirwvpfivsuwp2m.streamlit.app"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
data = {'chat_id': CHAT_ID, 'text': message}
requests.post(url, data=data)
print("✅ Telegram 전송 완료!")
