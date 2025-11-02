from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.constants import ParseMode
import os
import logging

# Logging sozlamalari
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# 🔹 Bu yerga o'zingning tokiningni qo'y!
# Tokenni environment variable orqali olish xavfsizroq va serverda ishlash uchun standart
TOKEN = os.environ.get("TELEGRAM_TOKEN", "8382278583:AAH5lq07V5i3-SIaP2eFJ4YNbVYhTaDxB7Y")

# Server sozlamalari
# Render kabi serverlar PORT va URL ni environment variable orqali beradi
PORT = int(os.environ.get("PORT", 8080))
WEBHOOK_URL = os.environ.get("WEBHOOK_URL") # Render avtomatik beradi

# 🔸 /start buyrug'i
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.from_user.full_name

    # users.json faylini o'chirib tashladik, chunki bepul serverlarda fayl saqlanmaydi.
    # Foydalanuvchilar sonini hisoblash funksiyasi hozircha o'chirildi.
    # Agar keyinchalik ma'lumotlar bazasi (masalan, PostgreSQL) ulasak, bu funksiyani qayta tiklash mumkin.

    await update.message.reply_text(
        "🌟 Ассалому алайкум, илм севувчи дўст!\n\n"
        "📚 Бу бот сен учун кутубхона — жой, бу ерда сен илм, руҳ ва молиявий ривожланиш учун китоблар билан танишасан.\n\n"
        "🔥 Ҳар куни бир саҳифа — ҳар ой бир китоб, ҳар йилда янги сен!\n\n"
        "👇 Бошлаш учун буйруқлар:\n"
        "/kitoblar — 📖 Китоблар рўйхати\n"
        "/users — 👥 Фойдаланувчилар сони (Ҳозирча ishlamaydi, serverga ulash uchun o'chirildi)"
    )

# 🔸 /kitoblar buyrug'i
async def kitoblar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📚 <b>Китоблар рўйхати:</b>\n\n"
        "1️⃣ <b>«Ойнаи жаҳон» — Аҳмад Дониш</b>\n"
        "   ➤ Илм ва тафаккур ҳақида чуқур фикрлар.\n\n"
        "2️⃣ <b>«Қўрқма» — Абдулҳамид Чўлпон</b>\n"
        "   ➤ Эркинлик ва миллий руҳ ҳақида илҳомли асар.\n\n"
        "3️⃣ <b>«Сиқилган одам» — Ф. Достоевский</b>\n"
        "   ➤ Инсоннинг ички дунёси ва қалб кураши ҳақида.\n\n"
        "4️⃣ <b>«7 миллион долларлик хатолар» — Алекса Томсон</b>\n"
        "   💰 Ҳақиқий молиявий фикрлаш ва хатолардан сабоқ олиш ҳақида мотивацион китоб.\n"
        "   📘 Бу китоб сени пул билан муносабатингни ўзгартиришга илҳомлантиради!"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.HTML)

# 🔸 /users buyrug'i
async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # users.json fayli o'chirildi. Bu funksiya serverda ishlamaydi.
    await update.message.reply_text(
        "⛔ Узр, фойдаланувчилар сонини ҳисоблаш функцияси вақтинча ўчирилди.\n"
        "Бу, ботни бепул серверга улаш учун зарур эди, чунки бепул серверлар маълумотларни сақламайди.\n"
        "Кейинчалик маълумотлар базаси уланса, бу функция қайта тикланади."
    )

# 🔹 Ботни ишга туширамиз
def main():
    """Bosh funksiya"""
    if not TOKEN:
        logger.error("TELEGRAM_TOKEN topilmadi. Iltimos, environment variable ni sozlang.")
        return

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("kitoblar", kitoblar))
    app.add_handler(CommandHandler("users", users))

    # Webhook rejimini sozlash
    if WEBHOOK_URL:
        logger.info(f"Webhook rejimida ishga tushirilmoqda. URL: {WEBHOOK_URL}, Port: {PORT}")
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=TOKEN,
            webhook_url=f"{WEBHOOK_URL}/{TOKEN}"
        )
    else:
        # Agar WEBHOOK_URL sozlanmagan bo'lsa, polling rejimida ishga tushirish (faqat lokal test uchun)
        logger.info("WEBHOOK_URL topilmadi. Polling rejimida ishga tushirilmoqda (faqat lokal test uchun).")
        app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
