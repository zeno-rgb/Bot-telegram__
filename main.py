# main.py
from keep_alive import keep_alive
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests
import re

BOT_TOKEN = "8199253435:AAH59wbbIxbCCi1PtYpy8GNuHx9t_TSlN4U"  # <-- Dán token bot vào đây
API_URL = "https://tikwm.com/api/"

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "───────────────────────\n"
        "📎 <b>© Bản Quyền Bot Thuộc Về @zenotele15</b> 🌹\n"
        "───────────────────────\n"
        "📥 <b>Tải Video TikTok Không Có Logo</b> 📥\n"
        "───────────────────────\n"
        "📎 Bot Chỉ Tải Được Video Dưới 1 Phút Thôi Nha Nữa 🎬\n"
        "───────────────────────\n"
        "🥰 Chúc Bạn Xem Video Không Có Logo Vui Vẻ 🥰\n"
        "───────────────────────\n"
        "👉 Bạn Hãy Gõ <b>/help</b> Để Biết Cách Tải Video Không Logo nhé 👈"
    )
    await update.message.reply_html(msg)

# /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "📌 <b>Bạn Chỉ Cần Gửi Link Video TikTok, Bot Sẽ Tự Động Tải Video Không Logo Cho Bạn 🥰.</b>\n\n"
        "🌐 <b>Ví dụ:</b> https://vt.tiktok.com/abc123/"
    )
    await update.message.reply_html(msg)

# Tự động phát hiện và xử lý video TikTok
async def detect_tiktok_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    match = re.search(r"(https?://(?:www\.)?tiktok\.com/\S+|https?://vt\.tiktok\.com/\S+)", text)
    if match:
        link = match.group(0)
        await update.message.reply_text("⏳ Đợi Xíu Nha... Bot Đang Xử Lý Video Cho Bạn 🎬😊")
        try:
            response = requests.get(API_URL, params={"url": link})
            data = response.json()
            if data.get("code") != 0:
                await update.message.reply_text("❌ Không tìm thấy video hoặc link sai.")
                return

            video_url = data["data"]["play"]
            caption = f"🎉 Đây Là Video Bạn Cần Nè 😊:\n📎 <b>Caption:</b> {data['data'].get('title', 'Không có')}"
            await update.message.reply_video(video=video_url, caption=caption, parse_mode="HTML")
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi tải video: {e}")
    else:
        await update.message.reply_text("⚠️ Vui lòng gửi link TikTok hợp lệ để bot xử lý!")

# Khởi chạy bot
keep_alive()  # Gọi keep_alive trước khi chạy bot

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), detect_tiktok_link))

app.run_polling()
import time
while True:
    time.sleep(10)
