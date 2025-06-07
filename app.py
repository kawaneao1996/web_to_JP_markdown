#!/usr/bin/env python3
"""
Streamlit Webアプリケーション
Web記事を日本語に翻訳してマークダウン形式で表示・ダウンロード
"""

import os
import tempfile
from typing import Optional

import streamlit as st

from main import WebToMarkdownTranslator


def initialize_session_state():
    """セッション状態の初期化"""
    if "translated_content" not in st.session_state:
        st.session_state.translated_content = ""
    if "original_url" not in st.session_state:
        st.session_state.original_url = ""
    if "processing" not in st.session_state:
        st.session_state.processing = False


def get_filename_from_url(url: str) -> str:
    """URLからファイル名を生成"""
    import re
    from urllib.parse import urlparse

    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "")
    path = parsed.path.strip("/").replace("/", "_")

    filename = f"{domain}_{path}" if path else domain
    filename = re.sub(r"[^\w\-_.]", "_", filename)
    return f"{filename}.md"


def process_url(url: str, api_key: Optional[str] = None) -> str:
    """URLを処理してマークダウン内容を返す"""
    try:
        translator = WebToMarkdownTranslator(api_key=api_key)

        # HTMLコンテンツ取得
        html_content = translator.fetch_web_content(url)

        # 主要コンテンツ抽出
        main_content = translator.extract_main_content(html_content)

        # マークダウン変換
        markdown_content = translator.html_to_markdown(main_content)

        # 日本語翻訳
        translated_content = translator.translate_to_japanese(markdown_content)

        return translated_content

    except Exception as e:
        raise Exception(f"処理エラー: {str(e)}")


def main():
    """メイン関数"""
    st.set_page_config(
        page_title="Web記事 日本語翻訳ツール", page_icon="📝", layout="wide"
    )

    initialize_session_state()

    st.title("📝 Web記事 日本語翻訳ツール")
    st.markdown(
        "Web記事を取得して日本語に翻訳し、マークダウン形式で表示・ダウンロードできます。"
    )

    # サイドバー
    with st.sidebar:
        st.header("設定")

        # APIキー設定
        api_key = st.text_input(
            "Gemini APIキー",
            type="password",
            value=os.getenv("GEMINI_API_KEY", ""),
            help="省略時は環境変数GEMINI_API_KEYを使用",
        )

        if not api_key and not os.getenv("GEMINI_API_KEY"):
            st.warning("⚠️ Gemini APIキーが設定されていません")

    # メインエリア
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("🌐 URL入力")

        # URL入力フォーム
        url = st.text_input(
            "翻訳したいWebページのURLを入力してください",
            placeholder="https://example.com/article",
            value=st.session_state.original_url,
        )

        # 処理実行ボタン
        if st.button("🔄 翻訳実行", disabled=not url or st.session_state.processing):
            if not api_key and not os.getenv("GEMINI_API_KEY"):
                st.error("❌ Gemini APIキーを設定してください")
            else:
                st.session_state.processing = True
                st.session_state.original_url = url

                with st.spinner("処理中..."):
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    try:
                        status_text.text("🌐 URLを取得中...")
                        progress_bar.progress(25)

                        status_text.text("📄 コンテンツを抽出中...")
                        progress_bar.progress(50)

                        status_text.text("🈯 日本語に翻訳中...")
                        progress_bar.progress(75)

                        # 実際の処理
                        translated_content = process_url(url, api_key or None)

                        st.session_state.translated_content = translated_content

                        progress_bar.progress(100)
                        status_text.text("✅ 処理完了！")

                        st.success("🎉 翻訳が完了しました！")

                    except Exception as e:
                        st.error(f"❌ エラーが発生しました: {str(e)}")

                    finally:
                        st.session_state.processing = False

    with col2:
        st.subheader("📋 翻訳結果")

        if st.session_state.translated_content:
            # マークダウン表示エリア
            st.markdown("### プレビュー")

            # タブで表示切り替え
            tab1, tab2 = st.tabs(["📖 レンダリング表示", "📝 マークダウン表示"])

            with tab1:
                st.markdown(st.session_state.translated_content)

            with tab2:
                st.code(st.session_state.translated_content, language="markdown")

            # ダウンロードボタン
            st.markdown("### ダウンロード")

            filename = get_filename_from_url(st.session_state.original_url)

            st.download_button(
                label="📥 マークダウンファイルをダウンロード",
                data=st.session_state.translated_content,
                file_name=filename,
                mime="text/markdown",
            )

            # ファイル情報表示
            st.info(f"📄 ファイル名: {filename}")

        else:
            st.info("👆 URLを入力して翻訳を実行してください")

    # フッター
    st.markdown("---")
    st.markdown(
        "💡 **使い方**: URLを入力して翻訳実行ボタンを押すと、"
        "Web記事が日本語に翻訳されてマークダウン形式で表示されます。"
    )


if __name__ == "__main__":
    main()
