import os
from telegram.ext import Application, MessageHandler, filters
import pandas as pd
import re

BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
df = pd.read_csv('bible_100plan.csv')

async def handle_input(update, context):
    msg = update.message.text
    match = re.match(r'([가-힣]+)(\d+)\s+(\d+)', msg)
    if match:
        book, ch, count = match.groups()
        idx = df[(df['book'].str.contains(book)) & (df['chapter']==int(ch))].index[0]
        df.at[idx, 'read_count'] += int(count)
        df.to_csv('bible_100plan.csv', index=False)
        await update.message.reply_text(f"✅ {book}{ch} +{count}독")
    await update.message.reply_text("시편23 1 형식으로 입력하세요")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle_input))
app.run_polling()
