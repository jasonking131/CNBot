from __future__ import annotations

import asyncio
from dataclasses import dataclass
from loguru import logger
from telegram import Bot
from telegram.error import RetryAfter, TimedOut, NetworkError

@dataclass
class Destination:
    chat_id: int
    message_thread_id: int | None = None

async def send_text(
    bot: Bot,
    dest: Destination,
    text: str,
    disable_preview: bool = False,
) -> int:
    """
    Sends a message and returns Telegram message_id.
    Retries on flood waits and transient network errors.
    """
    max_attempts = 5
    for attempt in range(1, max_attempts + 1):
        try:
            msg = await bot.send_message(
                chat_id=dest.chat_id,
                text=text,
                message_thread_id=dest.message_thread_id,
                disable_web_page_preview=disable_preview,
            )
            logger.info(f"Posted to chat_id={dest.chat_id}, thread={dest.message_thread_id}, msg_id={msg.message_id}")
            return msg.message_id

        except RetryAfter as e:
            wait = int(getattr(e, "retry_after", 3))
            logger.warning(f"Flood wait: sleeping {wait}s (attempt {attempt}/{max_attempts})")
            await asyncio.sleep(wait)

        except (TimedOut, NetworkError) as e:
            wait = 2 * attempt
            logger.warning(f"Network issue: {e}. sleeping {wait}s (attempt {attempt}/{max_attempts})")
            await asyncio.sleep(wait)

    raise RuntimeError("Failed to post message after retries")
