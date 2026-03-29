#!/usr/bin/env python3
"""ChatGPT完全攻略ナビ - CLIエントリポイント

blog_engineのmainモジュールを使用し、config.pyとprompts.pyを渡す。

使い方:
    python main.py generate --keyword "ChatGPT 使い方" --category "ChatGPT 使い方"
    python main.py build
    python main.py deploy
    python main.py schedule
    python main.py keywords --category "ChatGPT 使い方"
    python main.py calendar --days 7
    python main.py dashboard
"""

import sys
import os

# blog_engineへのパスを追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# 自分自身のディレクトリもパスに追加（config, promptsのインポート用）
sys.path.insert(0, os.path.dirname(__file__))

from blog_engine.main import load_module, ensure_dirs
from pathlib import Path


def main():
    """CLIのメインエントリーポイント"""
    import argparse
    import logging

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    # configとpromptsを自動ロード
    base_dir = Path(__file__).parent
    config = load_module(str(base_dir / "config.py"), "blog_config")
    prompts = load_module(str(base_dir / "prompts.py"), "blog_prompts")
    ensure_dirs(config)

    # コマンドライン引数のパース
    parser = argparse.ArgumentParser(
        description="ChatGPT完全攻略ナビ - ブログ管理CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="実行するコマンド")

    # generate
    parser_gen = subparsers.add_parser("generate", help="記事を生成する")
    parser_gen.add_argument("--keyword", required=True, help="ターゲットキーワード")
    parser_gen.add_argument("--category", required=True, help="カテゴリ")

    # build
    subparsers.add_parser("build", help="サイトをビルドする")

    # deploy
    subparsers.add_parser("deploy", help="GitHub Pagesにデプロイする")

    # schedule
    subparsers.add_parser("schedule", help="スケジューラーを起動する")

    # keywords
    parser_kw = subparsers.add_parser("keywords", help="キーワードリサーチ")
    parser_kw.add_argument("--category", required=True, help="対象カテゴリ")
    parser_kw.add_argument("--count", type=int, default=10, help="取得数")

    # calendar
    parser_cal = subparsers.add_parser("calendar", help="コンテンツカレンダー生成")
    parser_cal.add_argument("--days", type=int, default=7, help="日数")
    parser_cal.add_argument("--output", help="JSON保存先パス")

    # dashboard
    subparsers.add_parser("dashboard", help="ダッシュボードを起動する")

    # topics
    subparsers.add_parser("topics", help="トピックの統計情報を表示する")

    # collect-topics
    subparsers.add_parser("collect-topics", help="トレンドトピックを収集する")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    # コマンド実行
    if args.command == "generate":
        from blog_engine.article_generator import ArticleGenerator
        from blog_engine.seo_optimizer import SEOOptimizer

        generator = ArticleGenerator(config)
        article = generator.generate_article(
            keyword=args.keyword, category=args.category, prompts=prompts
        )
        print(f"記事生成完了: {article.get('title', '不明')}")

        optimizer = SEOOptimizer(config)
        seo_result = optimizer.check_seo_score(article)
        print(f"SEOスコア: {seo_result.get('total_score', 0)}/100")

    elif args.command == "build":
        from site_generator import SiteGenerator
        gen = SiteGenerator(config)
        gen.build_site()

    elif args.command == "deploy":
        from blog_engine.deployer import GitHubPagesDeployer
        deployer = GitHubPagesDeployer(config)
        result = deployer.deploy()
        print(f"デプロイ結果: {result['status']}")

    elif args.command == "schedule":
        from blog_engine.scheduler import BlogScheduler
        scheduler = BlogScheduler(config, prompts)
        scheduler.start()

    elif args.command == "keywords":
        from blog_engine.keyword_researcher import KeywordResearcher
        researcher = KeywordResearcher(config, prompts)
        keywords = researcher.research_trending_keywords(args.category, count=args.count)
        for i, kw in enumerate(keywords, 1):
            print(f"  {i:2d}. {kw['keyword']} [ボリューム: {kw.get('volume', '-')}]")

    elif args.command == "calendar":
        from blog_engine.keyword_researcher import KeywordResearcher
        researcher = KeywordResearcher(config, prompts)
        calendar = researcher.get_content_calendar(days=args.days)
        for entry in calendar:
            print(f"  {entry.get('date', '-')} | {entry.get('category', '-')} | {entry.get('keyword', '-')}")

    elif args.command == "dashboard":
        import uvicorn
        from blog_engine.dashboard import create_app
        app = create_app(config, prompts)
        host = config.DASHBOARD_HOST
        port = config.DASHBOARD_PORT
        print(f"ダッシュボード起動: http://{host}:{port}")
        uvicorn.run(app, host=host, port=port)

    elif args.command == "topics":
        from topic_collector import TopicCollector
        collector = TopicCollector(config, prompts)
        stats = collector.get_stats()
        print(f"トピック統計:")
        print(f"  合計: {stats['total']}")
        print(f"  未処理: {stats['pending']}")
        print(f"  完了: {stats['completed']}")
        for cat, data in stats['by_category'].items():
            print(f"  {cat}: {data['pending']}件未処理 / {data['total']}件中")

    elif args.command == "collect-topics":
        from topic_collector import TopicCollector
        collector = TopicCollector(config, prompts)
        collector.collect_trending_topics()
        print("トピック収集完了")


if __name__ == "__main__":
    main()
