# ベースイメージの指定
FROM python:3.12

# 作業ディレクトリの設定
WORKDIR /app

# Pythonの依存関係をインストール
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースコードをコピー
COPY . /app/

# ポートの公開
EXPOSE 8000

# アプリケーションの起動
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

