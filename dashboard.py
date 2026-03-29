"""ChatGPT完全攻略ナビ - ダッシュボードラッパー

blog_engineのdashboardを使用する。
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from blog_engine.dashboard import create_app

__all__ = ["create_app"]
