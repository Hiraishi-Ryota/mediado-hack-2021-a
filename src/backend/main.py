from gensim import models
from janome.tokenizer import Tokenizer

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from books.router import router as book_router
from db import Base, engine

# レコメンドエンジンのセットアップ
try:
    model = models.Doc2Vec.load('doc2vec.model')
except:
    pass
tokenizer = Tokenizer()
vectors_path = "vectors.pkl"

# DBのセットアップ
Base.metadata.create_all(bind=engine)

# fast apiのセットアップ
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# books routerを登録する。
app.include_router(book_router)
# staticファイルのホスティング
app.mount("/static", StaticFiles(directory="static"), name="static")
