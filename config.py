"""ChatGPT完全攻略ナビ - ブログ固有設定"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

BLOG_NAME = "ChatGPT完全攻略ナビ"
BLOG_DESCRIPTION = "ChatGPTの使い方・GPT最新モデル情報・料金プラン比較・プロンプト術を毎日更新。初心者から上級者まで、ChatGPTを最大限活用するための日本語情報サイト。"
BLOG_URL = "https://musclelove-777.github.io/chatgpt-master-navi"
BLOG_TAGLINE = "ChatGPTを完全に使いこなすための日本語ガイド"
BLOG_LANGUAGE = "ja"

GITHUB_REPO = "MuscleLove-777/chatgpt-master-navi"
GITHUB_BRANCH = "gh-pages"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

OUTPUT_DIR = BASE_DIR / "output"
ARTICLES_DIR = OUTPUT_DIR / "articles"
SITE_DIR = OUTPUT_DIR / "site"
TOPICS_DIR = OUTPUT_DIR / "topics"

TARGET_CATEGORIES = [
    "ChatGPT 使い方",
    "ChatGPT 料金・プラン",
    "GPT最新モデル",
    "ChatGPT vs Claude",
    "ChatGPT API・開発",
    "ChatGPT 最新ニュース",
    "ChatGPT プロンプト術",
    "ChatGPT 活用事例",
]

THEME = {
    "primary": "#10a37f",       # OpenAIグリーン
    "accent": "#1a7f64",
    "gradient_start": "#10a37f",
    "gradient_end": "#0d8c6d",
    "dark_bg": "#0d1117",
    "dark_surface": "#161b22",
    "light_bg": "#f0fdf4",
    "light_surface": "#ffffff",
}

MAX_ARTICLE_LENGTH = 4000
ARTICLES_PER_DAY = 2
SCHEDULE_HOURS = [8, 19]

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-2.5-flash"

ENABLE_SEO_OPTIMIZATION = True
MIN_SEO_SCORE = 75
MIN_KEYWORD_DENSITY = 1.0
MAX_KEYWORD_DENSITY = 3.0
META_DESCRIPTION_LENGTH = 120
ENABLE_INTERNAL_LINKS = True

AFFILIATE_LINKS = {
    "ChatGPT Plus": {"url": "https://chat.openai.com", "text": "ChatGPT Plusに登録する", "description": "月額$20でGPT最新モデルが使い放題"},
    "ChatGPT Team": {"url": "https://chat.openai.com", "text": "ChatGPT Teamプラン", "description": "チーム向けの高機能プラン"},
    "OpenAI API": {"url": "https://platform.openai.com", "text": "OpenAI APIコンソール", "description": "開発者向けAPI管理画面"},
    "Udemy": {"url": "https://www.udemy.com", "text": "UdemyでChatGPT講座を探す", "description": "ChatGPT活用のオンライン講座"},
    "Amazon": {"url": "https://www.amazon.co.jp", "text": "AmazonでChatGPT関連書籍を探す", "description": "ChatGPT関連の書籍・参考書"},
    "楽天": {"url": "https://www.rakuten.co.jp", "text": "楽天でChatGPT関連書籍を探す", "description": "ChatGPT関連の書籍・参考書"},
}
AFFILIATE_TAG = "musclelove07-22"

ADSENSE_CLIENT_ID = os.environ.get("ADSENSE_CLIENT_ID", "")
ADSENSE_ENABLED = bool(ADSENSE_CLIENT_ID)

DASHBOARD_HOST = "127.0.0.1"
DASHBOARD_PORT = 8084

# Google Analytics (GA4)
GOOGLE_ANALYTICS_ID = "G-CSFVD34MKK"

# Google Search Console 認証ファイル
SITE_VERIFICATION_FILES = {
    "googlea31edabcec879415.html": "google-site-verification: googlea31edabcec879415.html",
}
