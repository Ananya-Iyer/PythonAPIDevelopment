from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


# where is our database located
# syntax:
#SQLALCHEMY_DATABASE_URL = "postgresql://<username>:password@<ip-address/hostname:portnumber>/<database_name>"

SQLALCHEMY_DATABASE_URL = "postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOSTNAME}:{DATABASE_PORT}/{DATABASE_NAME}".format(DATABASE_USERNAME=settings.DATABASE_USERNAME, DATABASE_PASSWORD=settings.DATABASE_PASSWORD,
                                                            DATABASE_HOSTNAME=settings.DATABASE_HOSTNAME, DATABASE_PORT=settings.DATABASE_PORT, DATABASE_NAME=settings.DATABASE_NAME)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()