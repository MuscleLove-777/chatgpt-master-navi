"""ChatGPT完全攻略ナビ - サイト生成ラッパー

blog_engineのSiteGeneratorを使用し、追加でrobots.txtを生成する。
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from blog_engine.site_generator import SiteGenerator as BaseSiteGenerator
from seo_optimizer import SEOOptimizer


class SiteGenerator(BaseSiteGenerator):
    """ChatGPTブログ用サイト生成クラス"""

    def build_site(self):
        """サイトをビルドし、追加でrobots.txtを生成する"""
        super().build_site()

        # robots.txt生成
        seo = SEOOptimizer(self.config)
        robots_content = seo.generate_robots_txt()
        robots_path = self.output_dir / "robots.txt"
        robots_path.write_text(robots_content, encoding="utf-8")
        print("  robots.txt生成完了")


__all__ = ["SiteGenerator"]
