from sqlalchemy import Column, String, Date, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create the base class for models
Base = declarative_base()

# Define the Pill model
class Pill(Base):
    __tablename__ = "pills"
    id = Column(Integer, primary_key=True, index=True)
    color = Column(String, nullable=False)
    dibujo = Column(String, nullable=False)
    info = Column(String, nullable=False)
    fecha = Column(Date, nullable=False)

# SQLite database URL
DATABASE_URL = "sqlite:///./pills.db"

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize the database
def init_db():
    Base.metadata.create_all(bind=engine)
