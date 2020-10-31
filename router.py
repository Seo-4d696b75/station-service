from fastapi import APIRouter, Depends
from starlette.requests import Request

from databases import Database

from db import get_connection, Station

router = APIRouter()

@router.get("/api/")
async def api_root(request: Request):
  	return {"msg":"this is api endpoint"}

@router.get("/api/station")
async def api_root(code: int, database: Database = Depends(get_connection)):
	query = Station.select().where(Station.columns.code == code)
	data = await database.fetch_one(query)
	return data