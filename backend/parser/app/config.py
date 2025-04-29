# app/config.py
from dotenv import load_dotenv
import os

load_dotenv()  # picks up .env in repo root
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DB = os.getenv("NOTION_DB")


if not OPENAI_API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY")
if not NOTION_TOKEN or not NOTION_DB:
    raise RuntimeError("Missing NOTION_TOKEN/NOTION_DB")
