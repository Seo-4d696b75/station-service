from py.db import DataInfo
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

class DataInfoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = DataInfo
        ordered = True
    
    updated_at = fields.Function(lambda obj: obj.updated_at.isoformat())
