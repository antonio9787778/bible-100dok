import pandas as pd
import re
from telegram.ext import Application, MessageHandler, filters, CommandHandler
import os

TOKEN = "YOUR_BOT_TOKEN"

df = pd.read_csv('bible_plan.csv')

async def status(update, context):
    total = df['read_count'].sum()
    gu = df[df['testament']=='구약']['read_count'].sum()
    await update.message.reply_text(
        f"📖 100독 진행\n"
        f"총계: {total:,}/118,900 ({total/118900*100:.1f}%)\n"
        f"구약: {gu:,}/92,900\n"
        f"신약: {total-gu:,}/26,000\n"
        f"최근: {df[df['read_count']>0].tail(1).to_dict('records')}"
    )

async def update_count(update, context):
    msg = update.message.text
    match = re.match(r'([가-힣]+)(\d+)\s*(\d*)', msg)
    if match:
        book, ch, count = match.groups()
        ch = int(ch)
        count = int(count) if count else 1
        
        idx = df[(df['book'].str.contains(book, na=False)) & (df['chapter']==ch)].index
        if len(idx) > 0:
            df.at[idx[0], 'read_count'] = count
            df.to_csv('bible_plan.csv', index=False)
            total = df['read_count'].sum()
            await update.message.reply_text(f"✅ {book}{ch}장 {count}독\n총 {total:,}")
        else:
            await update.message.reply_text("❌ 장 못 찾음")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("status", status))
app.add_handler(MessageHandler(filters.TEXT, update_count))
app.run_polling()
