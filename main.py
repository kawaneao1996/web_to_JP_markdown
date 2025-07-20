#!/usr/bin/env python3
"""
Web記事を日本語に翻訳してマークダウン形式で出力するアプリケーション
"""

import argparse
import os
import sys
from typing import Optional

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from google import genai
from markdownify import markdownify as md  # type: ignore


class WebToMarkdownTranslator:
    """Web記事を取得し、日本語に翻訳してマークダウン形式で出力するクラス"""

    def __init__(self, api_key: Optional[str] = None):
        """
        初期化

        Args:
            api_key: Gemini APIキー（省略時は環境変数から取得）
        """
        if api_key is None:
            api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "Gemini APIキーが設定されていません。"
                "GEMINI_API_KEY環境変数を設定してください。"
            )

        self.client = genai.Client(api_key=api_key)

    def fetch_web_content(self, url: str) -> str:
        """
        URLからHTMLコンテンツを取得

        Args:
            url: 取得するWebページのURL

        Returns:
            HTMLコンテンツ

        Raises:
            requests.RequestException: Web取得エラー
        """
        try:
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                )
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.text or ""
        except requests.RequestException as e:
            raise requests.RequestException(f"Web取得エラー: {e}")

    def extract_main_content(self, html: str) -> str:
        """
        HTMLから主要コンテンツを抽出

        Args:
            html: HTMLコンテンツ

        Returns:
            抽出されたテキストコンテンツ
        """
        soup = BeautifulSoup(html, "html.parser")

        # 不要な要素を削除
        for element in soup(["script", "style", "nav", "header", "footer", "aside"]):
            element.decompose()

        # 主要コンテンツの抽出を試行（優先順位順）
        main_selectors = [
            "article",
            "main",
            '[role="main"]',
            ".content",
            ".post-content",
            ".entry-content",
            ".article-content",
        ]

        for selector in main_selectors:
            main_content = soup.select_one(selector)
            if main_content:
                return str(main_content)

        # 見つからない場合はbodyを使用
        body = soup.find("body")
        if body:
            return str(body)

        return str(soup)

    def translate_to_japanese(self, content: str) -> str:
        """
        マークダウンコンテンツを日本語に翻訳

        Args:
            content: 翻訳するマークダウンコンテンツ

        Returns:
            日本語に翻訳されたマークダウンコンテンツ
        """
        prompt = f"""
以下のマークダウンコンテンツを日本語に翻訳してください。
マークダウンの書式（#、*、[]()など）は保持し、テキスト部分のみを自然な日本語に翻訳してください。
技術的な用語や固有名詞は適切に日本語化してください。
URLやコードブロックはそのまま保持してください。
ただしコードブロックの言語が明記されていない場合は、推測してください。

{content}
"""

        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash", contents=prompt
            )
            return response.text or ""
        except Exception as e:
            raise Exception(f"翻訳エラー: {e}")

    def html_to_markdown(self, html: str) -> str:
        """
        HTMLをマークダウンに変換

        Args:``
            html: HTMLコンテンツ

        Returns:
            マークダウン形式のテキスト
        """
        return md(html, heading_style="ATX", bullets="-")  # type: ignore

    def process_url(self, url: str, output_path: str) -> None:
        """
        URLを処理してマークダウンファイルを出力

        Args:
            url: 処理するURL
            output_path: 出力ファイルパス
        """
        print(f"URLを取得中: {url}")
        html_content = self.fetch_web_content(url)

        print("主要コンテンツを抽出中...")
        main_content = self.extract_main_content(html_content)

        print("マークダウンに変換中...")
        markdown_content = self.html_to_markdown(main_content)

        print("日本語に翻訳中...")
        translated_content = self.translate_to_japanese(markdown_content)

        print(f"ファイルに出力中: {output_path}")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(translated_content)

        print("処理完了！")

    def process_url_to_markdown(self, url: str) -> str:
        """
        URLを処理してマークダウン形式のコンテンツを返す

        Args:
            url: 処理するURL

        Returns:
            マークダウン形式のコンテンツ
        """
        html_content = self.fetch_web_content(url)
        main_content = self.extract_main_content(html_content)
        markdown_content = self.html_to_markdown(main_content)
        translated_content = self.translate_to_japanese(markdown_content)
        return translated_content

    def translate_text_to_japanese(self, text: str) -> str:
        """
        マークダウンテキストを直接日本語に翻訳

        Args:
            text: 翻訳するマークダウンテキスト

        Returns:
            日本語に翻訳されたマークダウンテキスト
        """
        return self.translate_to_japanese(text)


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="Web記事やテキストを日本語に翻訳してマークダウン形式で出力"
    )
    parser.add_argument(
        "-i", "--input", required=True,
        help="翻訳するWebページのURLまたはテキストファイルのパス"
    )
    parser.add_argument(
        "-o", "--output", required=True, help="出力するマークダウンファイルのパス"
    )
    parser.add_argument(
        "--text", action="store_true",
        help="入力をテキストファイルとして処理（URLではなく）"
    )
    parser.add_argument(
        "--api-key", help="Gemini APIキー（省略時は環境変数GEMINI_API_KEYを使用）"
    )

    args = parser.parse_args()

    try:
        translator = WebToMarkdownTranslator(api_key=args.api_key)
        
        if args.text:
            # テキストファイルを読み込んで翻訳
            print(f"テキストファイルを読み込み中: {args.input}")
            with open(args.input, "r", encoding="utf-8") as f:
                text_content = f.read()
            
            print("日本語に翻訳中...")
            translated_content = translator.translate_text_to_japanese(text_content)
            
            print(f"ファイルに出力中: {args.output}")
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(translated_content)
            
            print("処理完了！")
        else:
            # URLから翻訳（従来の処理）
            translator.process_url(args.input, args.output)
            
    except Exception as e:
        print(f"エラー: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    load_dotenv()
    main()
