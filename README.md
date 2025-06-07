# web_to_JP_markdown

Web の URL を入力するとその内容を日本語に翻訳し、マークダウン形式で出力するアプリケーション。

## 処理の流れ

1. URL 先の HTML を取得
2. HTML をパースして、ボディないし、記事の DOM を特定し抽出する
3. 英語を日本語に翻訳し、マークダウン形式で出力する

## 使い方

1. 依存関係をインストール

   ```sh
   pip install -r requirements.txt
   ```

2. アプリケーションを実行

   ### CLI アプリ

   ```sh
   python main.py -i "URL" -o "./example.md"
   ```

   ### Web アプリ

   ```sh
   streamlit run app.py
   ```

   ブラウザで Web アプリが起動し、URL の入力、翻訳結果の表示、マークダウンファイルのダウンロードが可能です。
