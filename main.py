from fastapi import FastAPI
from api import edit

app = FastAPI(title="PDF Editor MVP")

app.include_router(edit.router)
