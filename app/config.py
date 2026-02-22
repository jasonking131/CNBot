from __future__ import annotations
from pathlib import Path
import os
import yaml
from dotenv import load_dotenv

load_dotenv()

def project_root() -> Path:
    return Path(__file__).resolve().parent.parent

def load_config() -> dict:
    cfg_path = project_root() / "config" / "config.yaml"
    data = {}
    if cfg_path.exists():
        with cfg_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

    data.setdefault("telegram", {})
    env_token = os.getenv("BOT_TOKEN")
    if env_token:
        data["telegram"]["bot_token"] = env_token

    return data