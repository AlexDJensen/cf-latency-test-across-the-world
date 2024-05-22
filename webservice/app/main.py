import time
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, PlainTextResponse

app = FastAPI()
FAVICON_PATH = "/code/app/static/favicon.ico"
LOREM_IPSUM = "/code/app/static/lorem_ipsum.txt"


BIG_TEXT = open(LOREM_IPSUM).read()
BIG_TEXT = BIG_TEXT * 100


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(round(process_time, 9))
    return response


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "welcome!"}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(FAVICON_PATH)


@app.get("/lorem_on_hit", response_class=PlainTextResponse())
async def lorem():
    big_text = open(LOREM_IPSUM).read()

    big_text = big_text * 100

    return PlainTextResponse(content=big_text, media_type="text/plain")


@app.get("/lorem_prepped", response_class=PlainTextResponse())
async def lorem_prepped():

    return PlainTextResponse(content=BIG_TEXT, media_type="text/plain")
