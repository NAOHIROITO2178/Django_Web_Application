# ベースイメージの指定
FROM python:3.12

# 作業ディレクトリの設定
WORKDIR /app

# 環境変数の設定
ENV PYTHONUNBUFFERED 1

# Pythonの依存関係をインストール
COPY requirements.txt /app/
RUN apt-get update && apt-get install -y \
    iputils-ping \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    && pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースコードをコピー
COPY . /app/

# ポートの公開
EXPOSE 8000

# ユーザーの作成
RUN useradd -m myuser

# ユーザーの切り替え
USER myuser

# アプリケーションの起動
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
