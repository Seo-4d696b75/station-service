# Station-Service

日本中の駅・路線データへの簡潔なアクセス手段を提供します. ここで扱うデータは[GitHub station_database](https://github.com/Seo-4d696b75/station_database)で管理されています.

## Deploy

[heroku](https://station-service.herokuapp.com/api/docs)にホストされる  


## Update Data

app起動時にデータの最新バージョンを確認して必要ならDB・インメモリデータを更新する [Dynoのライフサイクル](https://jp.heroku.com/dynos/lifecycle)

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