from pydantic import BaseModel, Field
import datetime

class DataInfoOut(BaseModel):
    data_version: int = Field(..., description="データバージョン [station_databaseリポジトリの最新データ](https://github.com/Seo-4d696b75/station_database/blob/master/latest_info.json)")
    updated_at: datetime.datetime = Field(..., description="現在のデータバージョンに更新された日時")

class BaseStationOut(BaseModel):
    code: int = Field(..., description="駅コード")
    id: str = Field(..., description="駅ID")
    name: str = Field(..., description="駅の名称")
    original_name: str = Field(..., description="駅名称のうち重複防止の接尾語を取り除いた名前")
    name_kana: str = Field(..., description="駅名称のかな表記（駅名重複防止のための接尾語のかな表記は含まず・一部ひらがな以外の記号を含む）")
    prefecture: int = Field(..., description="駅所在地の[都道府県コード](https://www.soumu.go.jp/denshijiti/code.html)")


class StationOut(BaseStationOut):
    lat: float = Field(..., description="駅所在地の緯度（オイラー角）")
    lng: float = Field(..., description="駅所在地の経度（オイラー角）")
    postal_code: str = Field(..., description="駅所在地の郵便番号")
    address: str = Field(..., description="駅所在地の住所")
    closed: bool = Field(..., description="廃駅なら`true`")
    open_date: str = Field(None, description="駅開業年月日")
    closed_date: str = Field(None, description="駅廃止年月日")
    attr: str = Field(..., description="駅の属性値")

class BaseLineOut(BaseModel):
    code: int = Field(..., description="路線コード")
    id: str = Field(..., description="路線ID")
    name: str = Field(..., description="路線の名称")
    name_kana: str = Field(..., description="路線名称のかな表記（括弧などの記号はそのまま）")

class LineOut(BaseLineOut):
    name_formal: str = Field(None, description='路線名の正式名称 `name`と同一の場合は省略')
    station_size: int = Field(..., ge=1, description='路線に登録されている駅数')
    company_code: int = Field(None, description='運行会社コード')
    color: str = Field(None, description='路線カラーコード `#[0-9A-F]\{6\}`')
    symbol: str = Field(None, description='路線記号')
    closed: bool = Field(..., description='`true`なら廃線')
    closed_date: str = Field(None, description='廃止年月日')

class NearestSearchOut(BaseModel):
    dist: float = Field(..., description='探索始点からの距離 `s:true`なら球面上で計算した距離[m] `s:false`なら緯度・経度の値から疑似的に計算したユークリッド距離（実際の距離ではない）')
    station: StationOut = Field(..., description='駅')