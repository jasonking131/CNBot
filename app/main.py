from __future__ import annotations

import argparse
import asyncio
from loguru import logger
from telegram import Bot

from app.config import load_config
from app.telegram.publish import Destination, send_text


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="cnbot")
    p.add_argument("--test-post", action="store_true")
    p.add_argument("--category", type=str, default=None)
    p.add_argument("--text", type=str, default="✅ CNBot test post")
    return p.parse_args()


def get_destination(cfg: dict, category_key: str) -> Destination:
    dests = cfg.get("destinations") or {}
    if category_key not in dests:
        raise KeyError(f"Category '{category_key}' not found in config.")
    d = dests[category_key]
    chat_id = int(d["chat_id"])
    thread_id = d.get("message_thread_id")
    thread_id = None if not thread_id else int(thread_id)
    return Destination(chat_id=chat_id, message_thread_id=thread_id)


async def run_test_post(category: str, text: str) -> None:
    cfg = load_config()
    token = cfg["telegram"]["bot_token"]

    if "PASTE_YOUR_BOT_TOKEN_HERE" in token:
        raise ValueError("You must set your bot token in config/config.yaml")

    bot = Bot(token=token)
    dest = get_destination(cfg, category)
    await send_text(bot, dest, text)


def main() -> None:
    args = parse_args()

    if args.test_post:
        if not args.category:
            raise SystemExit("Use --category <key>")
        logger.info("Posting test message...")
        asyncio.run(run_test_post(args.category, args.text))
        logger.info("Done.")
        return

    logger.info("CNBot booted.")


if __name__ == "__main__":
    main()