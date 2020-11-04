from db import Station, Line
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchema, auto_field


class StationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Station
        ordered = True

class ShortStationSchema(SQLAlchemySchema):
    class Meta:
        model = Station
        rodered = True
    
    code = auto_field()
    id = auto_field()
    name = auto_field()
    name_kana = auto_field()
    prefecture = auto_field()


class LineSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Line
        ordered = True

class ShortLineSchema(SQLAlchemySchema):
    class Meta:
        model = Line
        rodered = True
    
    code = auto_field()
    id = auto_field()
    name = auto_field()
    name_kana = auto_field()