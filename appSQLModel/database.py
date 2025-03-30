from sqlmodel import create_engine, Session, SQLModel

# Change to absolute path to be sure where the file is created
SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"  # Creates in the current directory

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

def get_session():
    with Session(engine) as session:
        yield session