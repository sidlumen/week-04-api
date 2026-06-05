import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables from a .env file in the project root
load_dotenv()

# Read the database connection URL (e.g. "postgresql://user:pass@localhost/db")
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# The engine is the entry point to the database — it manages connections
engine = create_engine(DATABASE_URL)

# SessionLocal is a factory for database sessions; each request gets its own session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the parent class all ORM models inherit from; it tracks the metadata
# (table names, columns, relationships) needed to create/query the schema
Base = declarative_base()


def get_db():
    """FastAPI dependency that yields a database session and guarantees cleanup."""
    db = SessionLocal()
    try:
        yield db
    finally:
        # Always close the session, even if the request raised an exception
        db.close()
