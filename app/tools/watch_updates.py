from __future__ import annotations

import time
import requests
from app.config import load_config

def main():
    cfg = load_config()
    token = cfg.get("telegram", {}).get("bot_token")
    if not token:
        raise RuntimeError("Missing telegram.bot_token in config/config.yaml")

    offset = None
    print("Watching updates... (CTRL+C to stop)")
    print("Step 1: DM the bot. Step 2: send message in CNVendors topic.\n")

    while True:
        params = {"timeout": 30}
        if offset is not None:
            params["offset"] = offset

        r = requests.get(
            f"https://api.telegram.org/bot{token}/getUpdates",
            params=params,
            timeout=60,
        )
        r.raise_for_status()
        data = r.json()

        for upd in data.get("result", []):
            offset = upd["update_id"] + 1

            msg = (
                upd.get("message")
                or upd.get("channel_post")
                or upd.get("edited_message")
                or upd.get("edited_channel_post")
            )

            print("\n=== UPDATE ===")
            if msg:
                chat = msg.get("chat", {})
                print("chat.type:", chat.get("type"))
                print("chat.title:", chat.get("title"))
                print("chat.id:", chat.get("id"))
                print("message_thread_id:", msg.get("message_thread_id"))
                print("text:", msg.get("text") or msg.get("caption"))
            else:
                print(upd)

        time.sleep(1)

if __name__ == "__main__":
    main()
