from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

from books.router import router as book_router

app = FastAPI()

# books routerを登録する。
app.include_router(book_router)
# staticファイルのホスティング
app.mount("/static", StaticFiles(directory="static"), name="static")
