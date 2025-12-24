from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine,URL
from core.config import setting
from pydantic import PostgresDsn

connection_url = URL.create(
    drivername="postgresql+psycopg2",
    username=setting.db_usr,        # "postgres"
    password=setting.db_pwd,        # "dproot"
    host=setting.db_host,           # "localhost"
    port=5432,                      # Default PostgreSQL port
    database=setting.db_name         
)



engine = create_engine(connection_url)
Sessionlocal =sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

