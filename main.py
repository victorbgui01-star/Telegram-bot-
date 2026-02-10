import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

openai.api_key = os.getenv("OPENAI_API_KEY")
TOKEN = os.getenv("TELEGRAM_TOKEN")

SYSTEM_PROMPT = """
Você é uma mulher chamada Luna.
Fala português do Brasil.
Conversa como uma pessoa real: casual, curta, às vezes irônica.
Use gírias leves.
Nunca diga que é IA ou bot.
"""

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return

    text = update.message.text

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        max_tokens=120,
        temperature=0.9
    )

    await update.message.reply_text(
        response.choices[0].message["content"]
    )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

if __name__ == "__main__":
    app.run_polling()
