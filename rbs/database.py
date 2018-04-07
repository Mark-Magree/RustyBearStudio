from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


Base = declarative_base()

class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    day = Column(String(32))
    month = Column(String(32))
    year = Column(String(32))
    street_name = Column(String(250))
    street_number = Column(String(250))
    city = Column(String(250))

class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True)
    file_name = Column(String(250), nullable=False)
    file_loc = Column(String(250), nullable=False)
    image_name = Column(String(250))
    description = Column(String())
    price = Column(Integer)
    sold = Column(Boolean, default=False)
    def __repr__(self):
        return f"<Image(name={self.file_name}, loc={self.file_loc}, price={self.price}, sold={self.sold})>"

engine = create_engine('sqlite:///rbs.db', echo=True)

if __name__ == "__main__":
    Base.metadata.create_all(engine)

