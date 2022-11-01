import uvicorn

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from db.postgres import database
from core.config import settings as s

from routers.base import router as base_router
from routers.version import router as version_router


app = FastAPI(
    title="Distributed config",
    # description=description,
    docs_url="/docs",
    redoc_url=None,
    openapi_url="/openapi.json",
    root_path_in_servers=False,
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1
    },
    contact={
        "name": "Gudynin Danila",
        "url": "https://ddgudynin.t.me",
        "email": "dggitdev@bk.ru",
    },
)

origins = [
    s.BACK_END_DOMAIN_ORIGIN,
    s.FRONT_END_DOMAIN_ORIGIN,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(base_router, tags=["Base CRUD"], prefix="/config")
app.include_router(version_router, tags=["Versioning"], prefix="/version")


@app.get("/healthcheck")
def healthchecker():
    return {"status": "true"}


@app.on_event("startup")
async def startup():    
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run(
        app, 
        port=8080, 
        host="0.0.0.0", 
        reload=False, 
        # use_colors=False,
        server_header=False,
    )