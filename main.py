import json

from fastapi import FastAPI, Request, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.middleware.cors import CORSMiddleware

from py.router import APIException, router

# defince app instance
api_setting = json.load(open('./api_setting.json','r',encoding='utf-8'))
app = FastAPI(
    title = api_setting['title'],
    version = api_setting['version'],
    description = api_setting['description'],
    openapi_tags = api_setting['meta_data'],
    docs_url = '/docs',
    openapi_url = '/openapi.json'
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

# 暫定的なリダイレクト対応
@app.exception_handler(404)
def recover_old_404(request: Request, exc: HTTPException):
    pathSegments = [s for s in request.url.path.split('/') if s != '']
    if len(pathSegments) > 0 and pathSegments[0] == 'api':
        return RedirectResponse(
            url=f"/{'/'.join(pathSegments[1:])}?{request.query_params}",
            status_code=301,
        )
    else:
        return JSONResponse(
            content={'detail': 'Not Found. See API docs for more details at /docs'},
            status_code=404,
        )

@app.on_event("startup")
async def startup():
    print('startup')

@app.on_event("shutdown")
async def shutdown():
    print('shutdown')

# users routerを登録する。
app.include_router(router)

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)
