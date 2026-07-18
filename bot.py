import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in data:
        data[user_id] = {
            "yes": 0,
            "no": 0,
            "streak": 0
        }

    await update.message.reply_text(
        "🌿 أهلاً بك\n\n"
        "سيصلك تذكير يومي لمتابعة قراءة سورة البقرة بإذن الله."
    )


async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):

    buttons = [
        [
            InlineKeyboardButton(
                "✅ نعم قرأتها",
                callback_data="yes"
            ),
            InlineKeyboardButton(
                "⏳ ليس بعد",
                callback_data="no"
            )
        ]
    ]

    await update.message.reply_text(
        "🌿 هل قرأت سورة البقرة اليوم؟",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    user_id = query.from_user.id

    if user_id not in data:
        data[user_id] = {
            "yes":0,
            "no":0,
            "streak":0
        }

    if query.data == "yes":
        data[user_id]["yes"] += 1
        data[user_id]["streak"] += 1
        msg = "💜 ما شاء الله، ربي يرضا عنك، وتقبل الله منك."

    else:
        data[user_id]["no"] += 1
        data[user_id]["streak"] = 0
        msg = "💛 وفقك الله، ما زال هناك وقت."

    await query.answer()
    await query.edit_message_text(msg)


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id not in data:
        await update.message.reply_text("لا يوجد بيانات.")
        return

    d = data[user_id]

    await update.message.reply_text(
        f"📊 الإحصائيات:\n\n"
        f"✅ قرأها: {d['yes']} يوم\n"
        f"❌ لم يقرأها: {d['no']} يوم\n"
        f"🔥 التتابع: {d['streak']} يوم"
    )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("ask", ask))
app.add_handler(CommandHandler("stats", stats))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()
