"""ChatGPT完全攻略ナビ - トピック収集モジュール

topics.jsonを管理し、新しいトピックの追加・ステータス管理を行う。
Gemini APIを使ってトレンドトピックを自動収集する。
"""

import json
import logging
from datetime import datetime
from pathlib import Path

from google import genai

logger = logging.getLogger(__name__)


class TopicCollector:
    """ChatGPT関連トピックの収集と管理"""

    def __init__(self, config, prompts=None):
        self.config = config
        self.prompts = prompts
        self.topics_file = config.BASE_DIR / "topics.json"
        self.client = genai.Client(api_key=config.GEMINI_API_KEY)
        self.model_name = config.GEMINI_MODEL

    def load_topics(self) -> dict:
        """topics.jsonからトピックを読み込む"""
        if self.topics_file.exists():
            with open(self.topics_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_topics(self, topics: dict):
        """topics.jsonにトピックを保存する"""
        with open(self.topics_file, "w", encoding="utf-8") as f:
            json.dump(topics, f, ensure_ascii=False, indent=2)
        logger.info("トピックを保存しました: %s", self.topics_file)

    def get_next_topic(self) -> dict | None:
        """未処理のトピックから優先度順に1件取得する"""
        topics = self.load_topics()
        priority_order = {"high": 0, "medium": 1, "low": 2}

        pending = []
        for category, topic_list in topics.items():
            for topic in topic_list:
                if topic.get("status") == "pending":
                    pending.append({
                        "category": category,
                        "keyword": topic["keyword"],
                        "priority": topic.get("priority", "medium"),
                    })

        if not pending:
            return None

        pending.sort(key=lambda t: priority_order.get(t["priority"], 1))
        return pending[0]

    def mark_completed(self, category: str, keyword: str):
        """トピックを完了済みに更新する"""
        topics = self.load_topics()
        if category in topics:
            for topic in topics[category]:
                if topic["keyword"] == keyword:
                    topic["status"] = "completed"
                    topic["completed_at"] = datetime.now().isoformat()
                    break
        self.save_topics(topics)

    def collect_trending_topics(self, count_per_category: int = 2) -> dict:
        """Gemini APIでトレンドトピックを収集し、topics.jsonに追加する"""
        logger.info("トレンドトピックを収集中...")

        categories_text = "\n".join(f"- {cat}" for cat in self.config.TARGET_CATEGORIES)

        prompt = (
            "ChatGPT（OpenAI）に関する最新のトレンドトピックを提案してください。\n\n"
            f"以下の各カテゴリについて、{count_per_category}個ずつ"
            "日本のユーザーが検索しそうなキーワードを提案してください。\n\n"
            f"カテゴリ一覧:\n{categories_text}\n\n"
            "以下のJSON形式で回答してください（説明不要）:\n"
            '{\n'
            '  "カテゴリ名": [\n'
            '    {"keyword": "検索キーワード", "title_hint": "記事タイトル案", "priority": "high/medium/low"}\n'
            '  ]\n'
            '}'
        )

        try:
            response = self.client.models.generate_content(
                model=self.model_name, contents=prompt
            )
            response_text = response.text.strip()

            if "```" in response_text:
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
                response_text = response_text.strip()

            new_topics = json.loads(response_text)

            # 既存トピックとマージ
            existing = self.load_topics()
            added_count = 0

            for category, topic_list in new_topics.items():
                if category not in existing:
                    existing[category] = []

                existing_keywords = {t["keyword"] for t in existing[category]}

                for topic in topic_list:
                    if topic["keyword"] not in existing_keywords:
                        topic["status"] = "pending"
                        existing[category].append(topic)
                        added_count += 1

            self.save_topics(existing)
            logger.info("%d件の新しいトピックを追加しました", added_count)
            return new_topics

        except Exception as e:
            logger.error("トピック収集に失敗: %s", e)
            return {}

    def get_stats(self) -> dict:
        """トピックの統計情報を取得する"""
        topics = self.load_topics()
        total = 0
        pending = 0
        completed = 0
        by_category = {}

        for category, topic_list in topics.items():
            cat_total = len(topic_list)
            cat_pending = sum(1 for t in topic_list if t.get("status") == "pending")
            cat_completed = sum(1 for t in topic_list if t.get("status") == "completed")

            total += cat_total
            pending += cat_pending
            completed += cat_completed
            by_category[category] = {
                "total": cat_total,
                "pending": cat_pending,
                "completed": cat_completed,
            }

        return {
            "total": total,
            "pending": pending,
            "completed": completed,
            "by_category": by_category,
        }
