from fastapi import FastAPI, Query, Request
from pydantic import BaseModel, Field
from typing import Optional, List
import sys
import pathlib
import os
from fastapi import Depends, HTTPException, status
from datetime import datetime
import json
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


# defince app instance
api_setting = json.load(open('./api_setting.json','r'))
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
            'status':'NG',
            'msg':'validation of request query failed.',
            'detail': exc.errors()}),
        headers={'WWW-Authenticate': 'Bearer error="invalid_request"'},
    )

# Base Error
class APIException(Exception):
    def __init__(self, code, msg, detail='', headers={}):
        self.code = code
        self.msg = msg
        self.detail = detail
        self.headers = headers

@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    return JSONResponse(
        status_code = exc.code,
        content = jsonable_encoder({
            'status':'NG',
            'msg': exc.msg,
            'detail': exc.detail }),
        headers=exc.headers
    )


@app.get("/api/", )
async def test():
    return {"status":"OK", "msg":"this is api endpoint"}

os.makedirs('tmp', exist_ok=True)
p_empty = pathlib.Path('tmp/app-initialized')
print(p_empty)