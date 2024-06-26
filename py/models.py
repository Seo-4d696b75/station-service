from pydantic import BaseModel, Field
from typing import Optional

class DataInfoOut(BaseModel):
    data_version: int = Field(
        ..., description="このAPIが返すデータのバージョン 基本的に[station_databaseリポジトリの最新データ](https://github.com/Seo-4d696b75/station_database)のバージョンに追従しますが、反映まで時間がかかる場合があります.")


class BaseStationOut(BaseModel):
    code: int = Field(..., description="駅コード")
    id: str = Field(..., description="駅ID")
    name: str = Field(..., description="駅の名称")
    original_name: str = Field(..., description="駅名称のうち重複防止の接尾語を取り除いた名前")
    name_kana: str = Field(...,
                           description="駅名称のかな表記（駅名重複防止のための接尾語のかな表記は含まず・一部ひらがな以外の記号を含む）")
    prefecture: int = Field(
        ..., description="駅所在地の[都道府県コード](https://www.soumu.go.jp/denshijiti/code.html)")
    extra: bool = Field(..., description="駅メモ実装なら`false`")


class StationOut(BaseStationOut):
    lat: float = Field(..., description="駅所在地の緯度（オイラー角）")
    lng: float = Field(..., description="駅所在地の経度（オイラー角）")
    postal_code: str = Field(..., description="駅所在地の郵便番号")
    address: str = Field(..., description="駅所在地の住所")
    closed: bool = Field(..., description="廃駅なら`true`")
    open_date: Optional[str] = Field(None, description="駅開業年月日")
    closed_date: Optional[str] = Field(None, description="駅廃止年月日")
    attr: Optional[str] = Field(None, description="駅の属性値（駅メモ実装でない場合はnull）")


class BaseLineOut(BaseModel):
    code: int = Field(..., description="路線コード")
    id: str = Field(..., description="路線ID")
    name: str = Field(..., description="路線の名称")
    name_kana: str = Field(..., description="路線名称のかな表記（括弧などの記号はそのまま）")
    extra: bool = Field(..., description="駅メモ実装なら`false`")


class LineOut(BaseLineOut):
    station_size: int = Field(..., ge=1, description='路線に登録されている駅数')
    company_code: Optional[int] = Field(None, description='運行会社コード')
    color: Optional[str] = Field(None, description='路線カラーコード `#[0-9A-F]{6}`')
    symbol: Optional[str] = Field(None, description='路線記号')
    closed: bool = Field(..., description='`true`なら廃線')
    closed_date: Optional[str] = Field(None, description='廃止年月日')


class NearestSearchOut(BaseModel):
    dist: float = Field(
        ..., description='探索始点からの距離 `s:true`なら球面上で計算した距離[m] `s:false`なら緯度・経度の値から疑似的に計算したユークリッド距離（実際の距離ではない）')
    station: StationOut = Field(..., description='駅')
