"""ChatGPT完全攻略ナビ - アフィリエイトリンク管理モジュール

ChatGPT特化のアフィリエイトリンクを記事に自動挿入する。
configのAFFILIATE_LINKS（辞書形式）に対応。
"""

import logging

logger = logging.getLogger(__name__)


class AffiliateManager:
    """ChatGPTブログ用アフィリエイトリンク管理"""

    def __init__(self, config, prompts=None):
        self.links = getattr(config, 'AFFILIATE_LINKS', {})
        self.amazon_tag = getattr(config, 'AFFILIATE_TAG', '')
        self.adsense_id = getattr(config, 'ADSENSE_CLIENT_ID', '')
        self.adsense_enabled = bool(self.adsense_id)

    def insert_affiliate_links(self, article: dict) -> dict:
        """記事にアフィリエイトリンクを挿入する"""
        content = article.get("content", "")
        category = article.get("category", "")
        keyword = article.get("keyword", "")

        relevant_links = self._find_relevant_links(category, keyword)

        if relevant_links:
            affiliate_section = self._build_affiliate_section(relevant_links, category)
            if "## まとめ" in content:
                content = content.replace("## まとめ", f"{affiliate_section}\n\n## まとめ")
            else:
                content += f"\n\n{affiliate_section}"
            article["content"] = content
            article["has_affiliate"] = True
            article["affiliate_count"] = len(relevant_links)
            logger.info("%d件のアフィリエイトリンクを挿入しました", len(relevant_links))
        else:
            article["has_affiliate"] = False
            article["affiliate_count"] = 0

        return article

    def _find_relevant_links(self, category: str, keyword: str) -> list:
        """カテゴリとキーワードに関連するリンクを選択する"""
        relevant = []
        keyword_lower = keyword.lower()

        # カテゴリやキーワードに基づいてリンクを選択
        for service_name, link_data in self.links.items():
            service_lower = service_name.lower()

            # ChatGPT Plus関連
            if "plus" in keyword_lower or "料金" in keyword_lower or "プラン" in keyword_lower:
                if "plus" in service_lower or "team" in service_lower:
                    relevant.append({"service": service_name, **link_data})

            # API関連
            if "api" in keyword_lower or "開発" in keyword_lower:
                if "api" in service_lower:
                    relevant.append({"service": service_name, **link_data})

            # 学習・書籍関連
            if "使い方" in keyword_lower or "入門" in keyword_lower or "始め方" in keyword_lower:
                if "udemy" in service_lower or "amazon" in service_lower or "楽天" in service_lower:
                    relevant.append({"service": service_name, **link_data})

        # 関連リンクが少ない場合、ChatGPT Plusと書籍を追加
        if len(relevant) < 2:
            for service_name in ["ChatGPT Plus", "Amazon", "Udemy"]:
                if service_name in self.links:
                    link_data = self.links[service_name]
                    if not any(r["service"] == service_name for r in relevant):
                        relevant.append({"service": service_name, **link_data})

        # 重複除去
        seen = set()
        unique = []
        for link in relevant:
            if link["service"] not in seen:
                seen.add(link["service"])
                unique.append(link)

        return unique[:5]

    def _build_affiliate_section(self, links: list, category: str) -> str:
        """アフィリエイトセクションのMarkdownを構築する"""
        section = "## 関連サービス・ツール\n\n"

        if "API" in category or "開発" in category:
            section += "ChatGPT APIの開発を始めるなら、以下のサービスがおすすめです。\n\n"
        elif "料金" in category or "プラン" in category:
            section += "ChatGPTの有料プランに興味がある方は、以下から詳細を確認できます。\n\n"
        else:
            section += "ChatGPTをもっと活用するために、以下のサービスがおすすめです。\n\n"

        for link in links:
            url = link.get("url", "")
            text = link.get("text", link.get("service", ""))
            description = link.get("description", "")

            if "amazon" in url.lower() and self.amazon_tag:
                separator = "&" if "?" in url else "?"
                url = f"{url}{separator}tag={self.amazon_tag}"

            section += f"- **[{text}]({url})** - {description}\n"

        section += "\n*※ 上記リンクからご利用いただくと、サイト運営の支援になります。*\n"
        return section

    def get_adsense_head_tag(self) -> str:
        """AdSenseのheadタグを返す"""
        if not self.adsense_enabled:
            return ""
        return f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={self.adsense_id}" crossorigin="anonymous"></script>'

    def get_adsense_article_ad(self) -> str:
        """AdSenseの記事内広告タグを返す"""
        if not self.adsense_enabled:
            return ""
        return f"""
<div style="text-align:center;margin:24px 0;">
  <ins class="adsbygoogle" style="display:block"
       data-ad-client="{self.adsense_id}" data-ad-slot="auto"
       data-ad-format="auto" data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
</div>"""
