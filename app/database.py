from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Change to absolute path to be sure where the file is created
SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"  # Creates in the current directory

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()  # Change from 'base' to 'Base'