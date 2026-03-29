"""ChatGPT完全攻略ナビ - SEO最適化モジュール

blog_engineのSEOOptimizerを拡張し、ChatGPTブログ特有のSEO最適化を行う。
JSON-LD構造化データ（BlogPosting, FAQPage, BreadcrumbList）の生成を含む。
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from blog_engine.seo_optimizer import SEOOptimizer as BaseSEOOptimizer


class SEOOptimizer(BaseSEOOptimizer):
    """ChatGPTブログ用のSEO最適化クラス"""

    def __init__(self, config):
        super().__init__(config)
        self.blog_url = config.BLOG_URL
        self.blog_name = config.BLOG_NAME

    def generate_blogposting_jsonld(self, article: dict) -> str:
        """BlogPosting JSON-LD構造化データを生成する"""
        slug = article.get("slug", "untitled")
        data = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": article.get("title", ""),
            "description": article.get("meta_description", ""),
            "url": f"{self.blog_url}/articles/{slug}.html",
            "datePublished": article.get("date", article.get("generated_at", "")),
            "dateModified": article.get("date", article.get("generated_at", "")),
            "author": {
                "@type": "Organization",
                "name": self.blog_name,
                "url": self.blog_url,
            },
            "publisher": {
                "@type": "Organization",
                "name": self.blog_name,
                "url": self.blog_url,
            },
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": f"{self.blog_url}/articles/{slug}.html",
            },
            "keywords": ", ".join(article.get("tags", [])),
            "articleSection": article.get("category", ""),
            "inLanguage": "ja",
        }
        return json.dumps(data, ensure_ascii=False, indent=2)

    def generate_faqpage_jsonld(self, article: dict) -> str:
        """FAQPage JSON-LD構造化データを生成する"""
        faq_items = article.get("faq", [])
        if not faq_items:
            return ""

        entities = []
        for item in faq_items:
            entities.append({
                "@type": "Question",
                "name": item.get("question", ""),
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": item.get("answer", ""),
                },
            })

        data = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": entities,
        }
        return json.dumps(data, ensure_ascii=False, indent=2)

    def generate_breadcrumb_jsonld(self, article: dict) -> str:
        """BreadcrumbList JSON-LD構造化データを生成する"""
        category = article.get("category", "未分類")
        title = article.get("title", "")
        slug = article.get("slug", "untitled")

        data = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "ホーム",
                    "item": self.blog_url,
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": category,
                    "item": f"{self.blog_url}/category/{category}.html",
                },
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": title,
                    "item": f"{self.blog_url}/articles/{slug}.html",
                },
            ],
        }
        return json.dumps(data, ensure_ascii=False, indent=2)

    def generate_all_jsonld(self, article: dict) -> list[str]:
        """全てのJSON-LD構造化データを生成する"""
        schemas = []

        blogposting = self.generate_blogposting_jsonld(article)
        if blogposting:
            schemas.append(blogposting)

        faq = self.generate_faqpage_jsonld(article)
        if faq:
            schemas.append(faq)

        breadcrumb = self.generate_breadcrumb_jsonld(article)
        if breadcrumb:
            schemas.append(breadcrumb)

        return schemas

    def generate_robots_txt(self) -> str:
        """robots.txtの内容を生成する"""
        return (
            "User-agent: *\n"
            "Allow: /\n"
            f"Sitemap: {self.blog_url}/sitemap.xml\n"
            f"Host: {self.blog_url}\n"
        )

    def generate_canonical_tag(self, article: dict) -> str:
        """canonical URLタグを生成する"""
        slug = article.get("slug", "untitled")
        return f'<link rel="canonical" href="{self.blog_url}/articles/{slug}.html">'

    def generate_ogp_tags(self, article: dict) -> str:
        """OGPメタタグを生成する"""
        slug = article.get("slug", "untitled")
        url = f"{self.blog_url}/articles/{slug}.html"
        tags = [
            f'<meta property="og:title" content="{article.get("title", "")}">',
            f'<meta property="og:description" content="{article.get("meta_description", "")}">',
            f'<meta property="og:url" content="{url}">',
            '<meta property="og:type" content="article">',
            f'<meta property="og:site_name" content="{self.blog_name}">',
            '<meta property="og:locale" content="ja_JP">',
        ]
        return "\n    ".join(tags)

    def generate_twitter_card_tags(self, article: dict) -> str:
        """Twitter Cardメタタグを生成する"""
        tags = [
            '<meta name="twitter:card" content="summary_large_image">',
            f'<meta name="twitter:title" content="{article.get("title", "")}">',
            f'<meta name="twitter:description" content="{article.get("meta_description", "")}">',
        ]
        return "\n    ".join(tags)
