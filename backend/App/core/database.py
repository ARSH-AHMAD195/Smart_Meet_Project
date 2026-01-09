from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from App.core.config import setting

engine = create_engine(
    setting.get_sql_database_url(), connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_db_and_tables():
    Base.metadata.create_all(bind=engine)       # This should be run on application startup