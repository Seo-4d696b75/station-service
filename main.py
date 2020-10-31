from fastapi import FastAPI, Query, Request
from pydantic import BaseModel, Field
from typing import Optional, List
import sys
from fastapi import Depends, HTTPException, status
from datetime import datetime
import json
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError

from router import router, APIException


# defince app instance
api_setting = json.load(open('./api_setting.json','r',encoding='utf-8'))
app = FastAPI(
    title = api_setting['title'],
    version = api_setting['version'],
    description = api_setting['description'],
    openapi_tags = api_setting['meta_data'],
    docs_url = '/api/docs',
    openapi_url = '/api/openapi.json'
)

# Handling RequestValidationError as status=400
@app.exception_handler(RequestValidationError)
async def validation_err_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code = status.HTTP_400_BAD_REQUEST,
        content = jsonable_encoder({
            'msg':'validation of request query failed.',
            'detail': exc.errors()})
    )


@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    return JSONResponse(
        status_code = exc.code,
        content = jsonable_encoder({
            'msg': exc.msg,
            'detail': exc.detail }),
        headers=exc.headers
    )

@app.exception_handler(SQLAlchemyError)
async def db_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code = status.HTTP_400_BAD_REQUEST,
        content = jsonable_encoder({
            'msg':'internal db error.',
            'detail': exc.errors()})
    )

@app.on_event("startup")
async def startup():
    print('startup')

@app.on_event("shutdown")
async def shutdown():
    print('shutdown')

# users routerを登録する。
app.include_router(router)
