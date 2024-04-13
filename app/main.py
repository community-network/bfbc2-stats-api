import pybfbc2stats
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_utils.tasks import repeat_every
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import RedirectResponse

from app import config
from app.cache import RedisClient
from app.exceptions import (
    PlayerNotFoundException,
    DataSourceException,
    NoPersonasException,
    TooManyPersonasException,
)
from app.fetch import FeslApiClient, TheaterApiClient
from app.router import router

app = FastAPI(
    title="FESL API",
    description='A <a href="https://fastapi.tiangolo.com/" target="_blank">FastAPI</a>-based wrapper around '
    '<a href="https://github.com/cetteup/pybfbc2stats" target="_blank">pybfbc2stats</a>, providing fast '
    "and easy access to Battlefield: Bad Company 2 stats and server lists "
    "(and other FESL/Theater features).",
    docs_url=None,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=[
        "Access-Control-Allow-Headers",
        "Origin",
        "Accept",
        "X-Requested-With",
        "Content-Type",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers",
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Methods" "Authorization",
        "X-Amz-Date",
        "X-Api-Key",
        "X-Amz-Security-Token",
    ],
)
app.include_router(router)
# Anyone requesting .../[endpoint]/ instead of just .../[endpoint] would get redirected to .../[endpoint],
# potentially leaking a CDN origin domain in the 307 redirect header => disable slash redirects
app.router.redirect_slashes = False


@app.get("/", include_in_schema=False)
async def read_root():
    response = RedirectResponse(url="/docs")
    return response


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html_cdn():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
        # swagger_ui_dark.css CDN link
        swagger_css_url="https://cdn.jsdelivr.net/gh/Itz-fork/Fastapi-Swagger-UI-Dark/assets/swagger_ui_dark.min.css",
        swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    )


@app.exception_handler(PlayerNotFoundException)
@app.exception_handler(pybfbc2stats.PlayerNotFoundError)
async def player_not_found_exception_handler(request, exc):
    headers = {"Cache-Control": "no-cache"}
    return JSONResponse(
        content={"errors": ["Player(s) not found"]}, headers=headers, status_code=404
    )


@app.exception_handler(pybfbc2stats.ServerNotFoundError)
async def server_not_found_exception_handler(request, exc):
    headers = {"Cache-Control": "no-cache"}
    return JSONResponse(
        content={"errors": ["Server not found"]}, headers=headers, status_code=404
    )


@app.exception_handler(NoPersonasException)
@app.exception_handler(TooManyPersonasException)
async def multi_persona_exception_handler(request, exc):
    headers = {"Cache-Control": "no-cache"}
    return JSONResponse(
        content={"errors": [str(exc)]}, headers=headers, status_code=422
    )


@app.exception_handler(pybfbc2stats.SearchError)
async def search_exception_handler(request, exc):
    headers = {"Cache-Control": "no-cache"}
    return JSONResponse(
        content={"errors": "Found no or too many results matching the search query"},
        headers=headers,
        status_code=422,
    )


@app.exception_handler(pybfbc2stats.TimeoutError)
async def timeout_exception_handler(request, exc):
    headers = {"Cache-Control": "no-cache"}
    return JSONResponse(
        content={"errors": "Timed out fetching data from source"},
        headers=headers,
        status_code=504,
    )


@app.exception_handler(pybfbc2stats.Error)
@app.exception_handler(pybfbc2stats.ParameterError)
@app.exception_handler(DataSourceException)
async def client_exception_handler(request, exc):
    headers = {"Cache-Control": "no-cache"}
    return JSONResponse(
        content={"errors": "Failed to fetch data from source"},
        headers=headers,
        status_code=502,
    )


@app.on_event("startup")
async def on_startup():
    redis_client = RedisClient()
    await redis_client.redis_connect()
    await maintain_fesl_instances()
    await maintain_theater_instances()


@repeat_every(seconds=10)
async def maintain_fesl_instances():
    client = FeslApiClient(config.CLIENT_TIMEOUT)
    await client.maintain_instances()


@repeat_every(seconds=10)
async def maintain_theater_instances():
    client = TheaterApiClient(config.CLIENT_TIMEOUT)
    await client.maintain_instances()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_config="../logging.yaml")
