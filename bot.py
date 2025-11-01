from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import json
import os

# 🔹 Tokenni shu yerga qo'y
TOKEN = "8382278583:AAH5lq07V5i3-SIaP2eFJ4YNbVYhTaDxB7Y"

USERS_FILE = "users.json"

# 🔸 Agar users.json bo‘lmasa, avtomatik yaratamiz
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump([], f)

# 🔸 /start buyrug‘i
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_name = update.effective_user.full_name

    with open(USERS_FILE, "r") as f:
        users = json.load(f)

    if user_id not in [u["id"] for u in users]:
        users.append({"id": user_id, "name": user_name})
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=4)
        await update.message.reply_text(f"Salom, {user_name}! Siz ro'yxatga qo'shildingiz ✅")
    else:
        await update.message.reply_text(f"Salom, {user_name}! Siz allaqachon ro'yxatdasiz 😎")

# 🔹 Botni ishga tushiramiz
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("🤖 Bot ishga tushdi...")
app.run_polling()
