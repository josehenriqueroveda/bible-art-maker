import os

from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from helpers.constants import API_IP
from helpers.constants import LIMITER
from routers.v1.art_maker_router import art_maker_router
from routers.v1.bible_router import bible_router
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from uvicorn import run


limiter = LIMITER
app = FastAPI(
    title="Bible Art-Maker API",
    description="""📖 API that creates customized images of Bible verses. Ideal for social media, presentations, and personal reflection.
              <p><strong>Developer</strong>: Jose Henrique Roveda<br/>""",
    version="0.0.1",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

origins = ["*"]
methods = ["*"]
headers = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=methods,
    allow_headers=headers,
    allow_credentials=True,
)

app.include_router(bible_router, prefix="/v1")
app.include_router(art_maker_router, prefix="/v1")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return """
    <html>
        <head>
            <title>Bible Art-Maker API</title>
        </head>
        <body>
            <h1>Bible Art-Maker API</h1>
            <p>📖 API that creates customized images of Bible verses. Ideal for social media, presentations, and personal reflection.</p>
            <p><strong>Developer</strong>: Jose Henrique Roveda<br/>
            <strong><a href=https://github.com/josehenriqueroveda/bible-art-maker">GitHub</a></strong>
        </body>
    </html>
        """


@app.get("/health", response_class=JSONResponse)
async def health(request: Request) -> JSONResponse:
    return JSONResponse({"status": "ok"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8777))
    run(app, host=API_IP, port=port)
