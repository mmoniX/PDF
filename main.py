"""FastAPI entrypoint: builds the application and registers all routers."""

from fastapi import FastAPI

from api.routers import edit, files

app = FastAPI(title="PDF Editor MVP")

app.include_router(edit.router)
app.include_router(files.router)
