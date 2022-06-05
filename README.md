# Station-Service

日本中の駅・路線データへの簡潔なアクセス手段を提供します.   
API Docs: https://station-service.herokuapp.com/api/docs

<img src="https://user-images.githubusercontent.com/25225028/172044813-31d2d023-f2d6-4752-b63c-c235acdc9708.png" width="500">

APIが扱うデータは[GitHub station_database](https://github.com/Seo-4d696b75/station_database)で管理されています.

<img src="https://user-images.githubusercontent.com/25225028/172044935-c49dce60-9a98-401b-8857-a51e8bad6f8f.png" height="120"/><img src="https://user-images.githubusercontent.com/25225028/172045357-3229a71b-0780-4565-971c-8f7e6aa519ea.png" height="120"/>  

<img src="https://user-images.githubusercontent.com/25225028/172044953-39a930eb-59ee-453e-8f1b-1da04e7cc4f0.png" height="120"/>

app起動時にデータの最新バージョンを確認して必要ならDB・インメモリデータを更新します [Dynoのライフサイクル](https://jp.heroku.com/dynos/lifecycle)

# 開発

## Conda環境のセットアップ
```bash
conda create --name station-service python=3.6.4
conda activate station-service
```

## パッケージのインストール
```bash
pip install -r requirements.txt
```

## VSCodeの設定
```json
{
  "python.condaPath": "/Users/${you}/opt/anaconda3/condabin/conda",
  "python.defaultInterpreterPath": "/Users/${you}/opt/anaconda3/envs/station-service/bin/python"
}
```

## DB認証情報の扱い
heroku Dyno での実行時では環境変数で認証情報が得られる  

ローカル環境・デバッグ実行時は次のようなシェルスクリプトを用意しておき読み出して使う

```bash
source db_credentials.sh
```

```sh:db_credentials.sh
export DB_USER=
export DB_PASSWORD=
export DB_HOST=
export DB_PORT=
export DB_DATABASE=
```