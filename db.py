from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_USER = 'admin'
DATABASE_PASSWORD = 'Abid@123'
DATABASE_HOST = 'localhost'
DATABASE_PORT = '5432'
DATABASE_NAME = "SampleDB"

DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
from sqlalchemy import Column, Integer, String

class ExampleModel(Base):
    __tablename__ = 'example_table'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)


Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    db = SessionLocal()
    new_entry = ExampleModel(name="Example Name", description="Example Description")
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    print(f"Inserted: {new_entry.name}, ID: {new_entry.id}")

