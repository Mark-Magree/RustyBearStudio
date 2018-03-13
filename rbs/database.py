from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


Base = declarative_base()

class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    date = Column(String(32))
    street_name = Column(String(250))
    street_number = Column(String(250))
    city = Column(String(250))

engine = create_engine('sqlite:///event_info.db', echo=True)

if __name__ == "__main__":
    Base.metadata.create_all(engine)

