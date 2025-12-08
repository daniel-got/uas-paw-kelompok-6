from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    "postgresql+psycopg2://app_prod_user:12345@localhost:5432/uas_pengweb"
)
Session = sessionmaker(bind=engine)
