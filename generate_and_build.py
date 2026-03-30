#!/usr/bin/env python3
"""GitHub Actions用一括実行スクリプト"""
import sys
import os

# blog_engineへのパスを追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from blog_engine.generate_and_build import run
import config
import prompts

if __name__ == "__main__":
    run(config, prompts)
