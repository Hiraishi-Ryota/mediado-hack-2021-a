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
  DATABASE_URL,
  connect_args={"check_same_thread": False},
  pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
Base.metadata.create_all(bind=engine)

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

  updated_at = Column(
    'updated_at',
    TIMESTAMP(timezone=True),
    onupdate=current_timestamp(),
    comment='最終更新日時',
  )