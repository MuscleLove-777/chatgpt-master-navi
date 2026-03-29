"""ChatGPT完全攻略ナビ - スケジューラーラッパー

blog_engineのBlogSchedulerを使用する。
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from blog_engine.scheduler import BlogScheduler

__all__ = ["BlogScheduler"]
