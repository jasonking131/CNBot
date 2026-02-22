from __future__ import annotations

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

from app.config import load_config


async def debug(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    chat = update.effective_chat

    print("\n=== TOPIC DEBUG ===")
    print("CHAT TYPE:", chat.type if chat else None)
    print("CHAT TITLE:", chat.title if chat else None)
    print("CHAT ID:", chat.id if chat else None)
    print("THREAD ID:", msg.message_thread_id if msg else None)
    print("TEXT:", (msg.text or msg.caption or "") if msg else None)
    print("===================\n")


def main():
    cfg = load_config()
    token = (cfg.get("telegram") or {}).get("bot_token")
    if not token:
        raise RuntimeError("Missing telegram.bot_token in config/config.yaml")

    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.ALL, debug))

    print("Listening... send a message INSIDE a topic now.")
    app.run_polling(close_loop=False)


if __name__ == "__main__":
    main()
