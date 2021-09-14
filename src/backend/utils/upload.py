import os
from pathlib import Path
import shutil
import sys
from tempfile import NamedTemporaryFile, SpooledTemporaryFile

BASE_DIR = os.getcwd()


def upload(filename: str, file: SpooledTemporaryFile, dir: str):
    """e_pub_fileをstaticに保存し、そのBASEDIR下のパスを返す"""
    try:
        with NamedTemporaryFile(delete=False, suffix=Path(filename).suffix, dir=dir) as tmp:
            shutil.copyfileobj(file, tmp)
            e_pub_path = Path(tmp.name)
    finally:
        file.close()
    return str(e_pub_path.relative_to(BASE_DIR))
