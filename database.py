# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Update this URL with your DB credentials
DATABASE_URL = "postgresql+psycopg2://postgres:Vamsi@localhost:5432/food_donation_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
