from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Get database URL from environment or use default
database_url = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://app_prod_user:12345@localhost:5432/uas_pengweb"
)

engine = create_engine(database_url)
Session = sessionmaker(bind=engine)
