"""ChatGPT完全攻略ナビ - プロンプト定義

ChatGPT（OpenAI）特化ブログ用のプロンプトを一元管理する。
"""

# ペルソナ設定
PERSONA = (
    "あなたはChatGPT専門のブロガーです。ChatGPT Plus・Team・Enterpriseの全プランを"
    "使い込んでいるパワーユーザーであり、OpenAI APIの開発経験も豊富です。"
    "初心者にもわかりやすく、上級者にも役立つ実践的な情報を発信しています。"
    "日本語ネイティブとして、日本のユーザー目線でChatGPTの活用法を解説します。"
)

# 記事フォーマット
ARTICLE_FORMAT = """
## この記事でわかること
- ポイント1
- ポイント2
- ポイント3

## 結論から言うと
（結論を1〜2文で端的に述べる）

## 本題
（メインコンテンツをH2/H3で構造化）

## 使い方手順
（具体的なステップバイステップの手順）

## 比較
（代替サービスや旧バージョンとの比較表）

## よくある質問（FAQ）
### Q1: ...
A1: ...
### Q2: ...
A2: ...
### Q3: ...
A3: ...

## まとめ
（要点整理と次のアクション提案）
"""

# カテゴリ別SEOキーワード設定
CATEGORY_PROMPTS = {
    "ChatGPT 使い方": {
        "primary_keywords": ["ChatGPT 使い方", "ChatGPT 始め方", "ChatGPT 無料", "ChatGPT 登録方法"],
        "secondary_keywords": ["ChatGPT 日本語", "ChatGPT スマホ", "ChatGPT アプリ", "ChatGPT ログイン"],
        "tone": "初心者に親切でわかりやすい解説",
    },
    "ChatGPT 料金・プラン": {
        "primary_keywords": ["ChatGPT 料金", "ChatGPT Plus", "ChatGPT 無料 有料 違い", "ChatGPT プラン比較"],
        "secondary_keywords": ["ChatGPT Team", "ChatGPT Enterprise", "ChatGPT Plus 解約", "ChatGPT 値段"],
        "tone": "料金の具体的な数字と比較表を重視",
    },
    "GPT最新モデル": {
        "primary_keywords": ["GPT-5", "GPT-5.4", "GPT-5.4 Mini", "GPT 最新モデル"],
        "secondary_keywords": ["GPT-4o", "GPT-4 Turbo", "GPTモデル 違い", "GPT 性能比較"],
        "tone": "技術的な正確さと実用的なベンチマーク情報",
    },
    "ChatGPT vs Claude": {
        "primary_keywords": ["ChatGPT Claude 比較", "ChatGPT vs Claude", "ChatGPT Claude どっち"],
        "secondary_keywords": ["AI チャット 比較", "Gemini 比較", "Claude 3.5", "ChatGPT 代替"],
        "tone": "公平で客観的な比較。両方のメリット・デメリットを明示",
    },
    "ChatGPT API・開発": {
        "primary_keywords": ["OpenAI API", "ChatGPT API", "OpenAI API 料金", "ChatGPT API 使い方"],
        "secondary_keywords": ["OpenAI API キー", "GPT API Python", "ChatGPT API 無料枠", "API 節約"],
        "tone": "開発者向けの実践的なコードサンプル付き解説",
    },
    "ChatGPT 最新ニュース": {
        "primary_keywords": ["ChatGPT 最新情報", "OpenAI ニュース", "ChatGPT アップデート", "ChatGPT 新機能"],
        "secondary_keywords": ["Sam Altman", "OpenAI 発表", "ChatGPT 障害", "GPT Store"],
        "tone": "速報性を重視。事実ベースで正確な情報",
    },
    "ChatGPT プロンプト術": {
        "primary_keywords": ["ChatGPT プロンプト", "プロンプトエンジニアリング", "ChatGPT 質問のコツ"],
        "secondary_keywords": ["プロンプト テンプレート", "ChatGPT 指示の出し方", "ChatGPT 回答精度", "プロンプト 書き方"],
        "tone": "すぐに使えるテンプレートとコピペ可能な例文",
    },
    "ChatGPT 活用事例": {
        "primary_keywords": ["ChatGPT 活用", "ChatGPT ビジネス", "ChatGPT 仕事", "ChatGPT 活用事例"],
        "secondary_keywords": ["ChatGPT 副業", "ChatGPT 効率化", "ChatGPT 自動化", "ChatGPT Excel"],
        "tone": "具体的なビジネスシーンでの成功事例と数字",
    },
}

# キーワードリサーチ用追加プロンプト
KEYWORD_PROMPT_EXTRA = (
    "ChatGPT関連の日本語ロングテールキーワードを意識してください。\n"
    "以下のような検索意図を持つキーワードを優先してください:\n"
    "- 「ChatGPT 〇〇 やり方」「ChatGPT 〇〇 方法」などのHowTo系\n"
    "- 「ChatGPT 〇〇 比較」「ChatGPT 〇〇 違い」などの比較系\n"
    "- 「ChatGPT 〇〇 2026」などの最新年度キーワード\n"
    "- 「ChatGPT 無料で〇〇」などのコスト意識系\n"
    "日本のChatGPTユーザーが実際に検索しそうなフレーズを重視してください。"
)

# ニュースソース
NEWS_SOURCES = [
    "OpenAI Blog (https://openai.com/blog)",
    "OpenAI Changelog (https://help.openai.com/en/articles/changelog)",
    "TechCrunch AI (https://techcrunch.com/category/artificial-intelligence/)",
    "The Verge AI (https://www.theverge.com/ai-artificial-intelligence)",
    "AI News JP (日本語AIニュースサイト各種)",
]

# FAQ構造化データを有効化
FAQ_SCHEMA_ENABLED = True


def build_keyword_prompt(config):
    """キーワード選定プロンプトを構築する"""
    categories_text = "\n".join(f"- {cat}" for cat in config.TARGET_CATEGORIES)
    return (
        f"{PERSONA}\n\n"
        "ChatGPT特化ブログ用のキーワードを選定してください。\n\n"
        "以下のカテゴリから1つ選び、そのカテゴリで今注目されている"
        "ChatGPT関連のトピック・キーワードを1つ提案してください。\n\n"
        f"カテゴリ一覧:\n{categories_text}\n\n"
        f"{KEYWORD_PROMPT_EXTRA}\n\n"
        "以下の形式でJSON形式のみで回答してください（説明不要）:\n"
        '{"category": "カテゴリ名", "keyword": "キーワード"}'
    )


def build_article_prompt(keyword, category, config):
    """ChatGPT特化記事用の生成プロンプトを構築する"""
    cat_config = CATEGORY_PROMPTS.get(category, {})
    primary_kws = ", ".join(cat_config.get("primary_keywords", [keyword]))
    secondary_kws = ", ".join(cat_config.get("secondary_keywords", []))
    tone = cat_config.get("tone", "わかりやすく実践的な解説")

    news_sources_text = "\n".join(f"- {src}" for src in NEWS_SOURCES)

    faq_instruction = ""
    if FAQ_SCHEMA_ENABLED:
        faq_instruction = (
            "\n【FAQ構造化データ】\n"
            "記事内に「よくある質問（FAQ）」セクションを必ず含めてください。\n"
            "Q&Aを3〜5個設定し、JSON-LD FAQPage構造化データとして出力できる形式にしてください。\n"
        )

    return f"""{PERSONA}

以下のキーワードに関する、読者がすぐに実践できるChatGPT活用記事を書いてください。

【基本条件】
- ブログ名: {config.BLOG_NAME}
- ブログ説明: {config.BLOG_DESCRIPTION}
- キーワード: {keyword}
- カテゴリ: {category}
- 言語: 日本語
- 文字数: {config.MAX_ARTICLE_LENGTH}文字程度
- トーン: {tone}

【SEOキーワード】
- 主要キーワード: {primary_kws}
- 副次キーワード: {secondary_kws}

【参考ニュースソース】
{news_sources_text}

【記事フォーマット】
{ARTICLE_FORMAT}

【SEO要件】
1. タイトルにキーワード「{keyword}」を必ず含めること
2. タイトルは32文字以内で魅力的に（クリック率を意識）
3. H1 → H2 → H3の見出し階層構造を厳密に守ること
4. キーワード密度は{config.MIN_KEYWORD_DENSITY}%〜{config.MAX_KEYWORD_DENSITY}%を目安に
5. メタディスクリプションは{config.META_DESCRIPTION_LENGTH}文字以内
6. canonical URL: {config.BLOG_URL}/articles/{{slug}}.html
7. 内部リンクのプレースホルダーを2〜3箇所に配置（{{{{internal_link:関連トピック}}}}の形式）
{faq_instruction}
【条件】
- {config.MAX_ARTICLE_LENGTH}文字程度
- 具体的な手順・スクリーンショットの位置指示を含める
- 料金は具体的な数字を明記（2026年最新の情報を使用）
- 比較セクションでは表形式を使用
- 読者がすぐにアクションを起こせるCTAを含める
- 日本語ユーザー向けの注意点（日本語対応状況、日本からの利用制限など）に触れる

【出力形式】
以下のJSON形式で出力してください。JSONブロック以外のテキストは出力しないでください。

```json
{{
  "title": "SEO最適化されたタイトル",
  "content": "# タイトル\\n\\n本文（Markdown形式）...",
  "meta_description": "120文字以内のメタディスクリプション",
  "tags": ["タグ1", "タグ2", "タグ3", "タグ4", "タグ5"],
  "slug": "url-friendly-slug",
  "faq": [
    {{"question": "質問1", "answer": "回答1"}},
    {{"question": "質問2", "answer": "回答2"}},
    {{"question": "質問3", "answer": "回答3"}}
  ]
}}
```

【注意事項】
- content内のMarkdownは適切にエスケープしてJSON文字列として有効にすること
- tagsは5個ちょうど生成すること
- slugは半角英数字とハイフンのみ使用すること
- faqは3〜5個生成すること
- 読者にとって実用的で具体的な内容を心がけること
- 「〜と言われています」のような曖昧な表現を避け、断定的に書くこと"""
