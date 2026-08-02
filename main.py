"""FastAPI entrypoint: builds the application and registers all routers."""

from fastapi import FastAPI

from api.routers import edit, files
from schemas import ServiceInfo

app = FastAPI(title="PDF Editor MVP", version="0.1.0")

app.include_router(edit.router)
app.include_router(files.router)


@app.get("/", response_model=ServiceInfo, tags=["Meta"])
def root() -> ServiceInfo:
    """Return the service name, version, and available /pdf endpoints."""
    endpoints = sorted(r.path for r in app.routes if r.path.startswith("/pdf"))
    return ServiceInfo(name=app.title, version=app.version, endpoints=endpoints)
