from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Створення бази
engine = create_engine("sqlite:///players.db")
Session = sessionmaker(bind=engine)
Base = declarative_base()
