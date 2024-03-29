# Station-Service

日本中の駅・路線データを簡単に取得できるREST APIです

- URL：https://api.station.seo4d696b75.com/
- [各エンドポイントの詳細はSwagger UIを参照してください](https://api.station.seo4d696b75.com/docs)

<img src="https://user-images.githubusercontent.com/25225028/172044813-31d2d023-f2d6-4752-b63c-c235acdc9708.png" width="500">

### データのソース
APIが扱うデータは[GitHub station_database](https://github.com/Seo-4d696b75/station_database)で管理されています.

### データの更新
Google Cloud Run のサービスは外部から再起動できない？ので、  
同じContainerイメージのまま新しいリビジョンで再デプロイする


### 使用技術
<img src="https://user-images.githubusercontent.com/25225028/172044935-c49dce60-9a98-401b-8857-a51e8bad6f8f.png" height="120"/><img src="https://user-images.githubusercontent.com/25225028/198833805-195dcb64-0d4c-4db6-ab30-d65e787a242a.png" height="120"/>

<img src="https://user-images.githubusercontent.com/25225028/172044953-39a930eb-59ee-453e-8f1b-1da04e7cc4f0.png" height="120"/>

Heroku から Google Cloud Run にデプロイ先を変更しました  

<img src="https://user-images.githubusercontent.com/25225028/198833929-a04f637b-ac0b-4f44-a3a4-3852c7a71d3a.png" width="400"/>

# 開発


## Dockerコンテナ環境（デプロイあり）
Google Cloud Runにデプロイするのに必要です

### gcloud CLIのセットアップ

リージョン指定は適宜読み替えて下さい

1. [インストール](https://cloud.google.com/sdk/docs/install?hl=ja)
2. Google Cloudを利用するアカウントでログイン
```bash
gcloud auth login
```

3. プロジェクトの指定
```bash
gcloud config set project ${PROJECT_ID}
gcloud config set run/region asia-northeast1
```

4. Dockerに認証情報をセット

```bash
gcloud auth configure-docker asia-northeast1-docker.pkg.dev
```

### イメージのbuild

1. Docker Desktopなどで使用する場合

```bash
docker build -t ${local_name}:${local_tag} . 
```

2. GCRにデプロイする場合

```bash
docker build -t ${local_name}:${local_tag} . --platform linux/amd64
```

### イメージのPush
[Google Artifact Registryを利用します](https://cloud.google.com/artifact-registry/docs/docker/pushing-and-pulling?hl=ja)

`tag=asia-northeast1-docker.pkg.dev/${project_id}/${repo}/${remote_name}:${remote_tag}`

```bash
docker tag ${local_name}:${local_tag} $tag
docker push $tag
```

### Google Cloud Runへのデプロイ
[Google Cloud Consoleから操作できます](https://cloud.google.com/run/docs/deploying?hl=ja#revision)



##　Conda環境（デプロイなし）

ローカルで手軽に実行・開発するのに便利です

**注意** HerokuからGoogle Cloud Runへの移行に伴いデプロイにはDockerイメージのビルドが必要です

### 環境のセットアップ
```bash
conda create --name station-service python=3.12
conda activate station-service
pip install -r requirements.txt
```

### ローカル実行
```bash
uvicorn main:app --host 0.0.0.0 --port 3003 --reload
```

### VSCodeのデバッグ設定
```json
{
  "python.condaPath": "/Users/${you}/opt/anaconda3/condabin/conda",
  "python.defaultInterpreterPath": "/Users/${you}/opt/anaconda3/envs/station-service/bin/python"
}
```
