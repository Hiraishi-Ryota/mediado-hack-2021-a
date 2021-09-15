# mediado-hack-2021-a

## バックエンドローカルに動作環境を用意(anaconda、別になんでもいい)

### 1. anaconda環境の準備(仮想環境を準備)

  anaconda promptより

  `conda create -n mediado python=3.8.11`

### 2. 上記環境に必要ライブラリをインストール(このブランチ上のrequirements.txtを利用)

  anaconda内の仮想環境のpromptから、`/backend`で、

  `pip install -r requirements.txt`

### 3. db準備-1(postgresqlの環境準備～接続)

  > Mac

    1. postgresのインストール
    `brew install postgresql`

    2. postgresの起動
    `brew services start postgresql`

### 4. postgresデータベースの接続

  `psql -h localhost -p 5432 -U postgres -d postgres`

  -> 初期状態ではpostgresユーザ(role)とpostgresデータベースが作成される

  -> -Uオプションと-dオプションでユーザとデータベースを設定している
  -> パスワードが求められたら、postgresを入力

  ※繋がらない場合:恐らく、ユーザ名が*(自PCのユーザ名)になっているため、以下を実施

  1. `psql -h localhost -p 5432 -U * -d postgres`によりdbに接続
  2. `create role postgres with superuser login password 'postgres';`の実行
  3. `alter role postgres createdb;`の実行

  -> これで、psql -h localhost -p 5432 -U postgres -d postgresに繋がるようになる

  -> \qでdbから抜けてpsql -h localhost -p 5432 -U postgres -d postgresでdbに接続

### 5. db準備-2(postgresqlのデータベースの作成)

※ postgresデータベースにpostgresロールでアクセスしている前提

`create database media_do_hack_2021;`でデータベースを作成

### local 起動

`uvicorn main:app --reload`

### 本番　起動

ワーカー数、スレッド数は要調整

`gunicorn --workers=4 --threads=2  -k uvicorn.workers.UvicornWorker main:app --log-level warning`