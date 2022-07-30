from os import getenv
from dotenv import load_dotenv

from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from pydantic import BaseModel
from fastapi_crudrouter import SQLAlchemyCRUDRouter

# from main import app

load_dotenv()

engine = create_engine(
    f'postgresql://{getenv("DB_USER")}:{getenv("DB_PASS")}@{getenv("DB_HOST")}:5432/{getenv("DB_NAME")}'
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    finally:
        session.close()


class UserCreate(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str


class User(UserCreate):
    id: int

    class Config:
        orm_mode = True


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), index=True, unique=True, nullable=False)
    email = Column(String(120), index=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)


Base.metadata.create_all(bind=engine)

router = SQLAlchemyCRUDRouter(
    schema=User,
    create_schema=UserCreate,
    db_model=UserModel,
    db=get_db,
    prefix='user'
)


