
import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from openai import AsyncOpenAI

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

chat_history = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✨ Welcome to AI Chatting Bot!\n\n"
        "Mujhse kuch bhi pooch sakte ho. 😊"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message = update.message.text

    if user_id not in chat_history:
        chat_history[user_id] = []

    history = chat_history[user_id]
    history.append({"role": "user", "content": message})

    try:
        response = await client.responses.create(
            model="gpt-5.5",
            instructions="You are a friendly AI assistant. Reply in the language used by the user.",
            input=history
        )

        answer = response.output_text

        history.append({"role": "assistant", "content": answer})
        chat_history[user_id] = history[-12:]

        await update.message.reply_text(answer)

    except Exception:
        await update.message.reply_text(
            "Sorry! Abhi kuch problem aa rahi hai. Thodi der baad try karo."
        )

def main():
    if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
        raise ValueError("API keys are missing!")

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
    )

    print("AI Chatting Bot Started!")
    app.run_polling()

if __name__ == "__main__":
    main()
  
