from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from app import get_filename_from_url
from main import WebToMarkdownTranslator

# FastMCPの初期化
mcp = FastMCP("web_to_jp_markdown")

load_dotenv()


@mcp.tool()
async def convert_url_to_jp_markdown(url: str) -> str:
    """URLのコンテンツを日本語に翻訳し、マークダウン形式で返す
    主要なHTMLコンテンツを抽出し、マークダウン形式に変換して日本語に翻訳します。

    Args:
        url (str): 翻訳するURL

    Returns:
        str: 日本語に翻訳されたマークダウン形式のコンテンツ
    """
    translator = WebToMarkdownTranslator()

    try:
        md = translator.process_url_to_markdown(url)

    except Exception as e:
        raise Exception(f"処理エラー: {str(e)}")

    return md


@mcp.tool()
async def get_markdown_filename(url: str) -> str:
    """URLからマークダウンファイル名を生成

    Args:
        url (str): URL

    Returns:
        str: マークダウンファイル名
    """
    return get_filename_from_url(url)


if __name__ == "__main__":
    mcp.run(transport="stdio")
