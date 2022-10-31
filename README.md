# Station-Service

日本中の駅・路線データへの簡潔なアクセス手段を提供します.   
API Docs: https://station-service-5bzhd44ozq-an.a.run.app/api/docs

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
1. [インストール](https://cloud.google.com/sdk/docs/install?hl=ja)
2. Google Cloudを利用するアカウントでログイン
```
gcloud auth login
```
3. プロジェクトの指定
```
gcloud config set project ${PROJECT_ID}
gcloud config set run/region asia-northeast1 // リージョン指定（任意）
```
4. Dockerに認証情報をセット
```
gcloud auth configure-docker
```

### イメージのbuild

1. Docker Desktopなどで使用する場合

```
docker build -t station-api-image:${version} . 
```

2. GCRにデプロイする場合

```
docker build -t asia.gcr.io/${PROJECT_ID}/station-api-image:${version} . --platform linux/amd64
```

### イメージのPush
Google Container Registryを利用します
```
docker push asia.gcr.io/${PROJECT_ID}/station-api-image:${version}
```

### Google Cloud Runへのデプロイ
[Google Cloud Consoleから操作できます](https://cloud.google.com/run/docs/deploying?hl=ja#revision)



##　Conda環境（デプロイなし）

ローカルで手軽に実行・開発するのに便利です

**注意** HerokuからGoogle Cloud Runへの移行に伴いデプロイにはDockerイメージのビルドが必要です

### Conda環境のセットアップ
```bash
conda create --name station-service python=3.6.4
conda activate station-service
```

### パッケージのインストール
```bash
pip install -r requirements.txt
```

### VSCodeの設定
```json
{
  "python.condaPath": "/Users/${you}/opt/anaconda3/condabin/conda",
  "python.defaultInterpreterPath": "/Users/${you}/opt/anaconda3/envs/station-service/bin/python"
}
```
