from sqlalchemy import create_engine, Column
from sqlalchemy.dialects.postgresql import INTEGER, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.functions import current_timestamp

DATABASE = 'postgresql'
USER = 'postgres'
PASSWORD = 'postgres'
HOST = 'localhost'
PORT = '5432'
DB_NAME = 'media_do_hack_2021'

DATABASE_URL = f'{DATABASE}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}'

engine = create_engine(
    DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class BasicModel(Base):
    """ベースモデル"""
    __abstract__ = True

    id = Column(
        INTEGER,
        primary_key=True,
        autoincrement=True,
    )

    created_at = Column(
        'created_at',
        TIMESTAMP(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
        comment='登録日時',
    )
