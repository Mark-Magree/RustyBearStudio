from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


Base = declarative_base()

class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    name = Column(String(), nullable=False)
    days = Column(Integer)
    time_start = Column(String())
    time_end = Column(String())
    day = Column(String())
    month = Column(String())
    month_txt = Column(String())
    time_start2 = Column(String())
    time_end2 = Column(String())
    day2 = Column(String())
    month2 = Column(String())
    month2_txt = Column(String())
    year = Column(String())
    street_name = Column(String())
    street_number = Column(String())
    city = Column(String())
    details = Column(String())
    def __repr__(self):
        return f"<Event(name={self.name}, days={self.days}, date={self.day}/{self.month}/{self.year}, address={self.street_number} {self.street_name}, {self.city})>"

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

engine = create_engine('sqlite:///rbs.db', echo=False)

if __name__ == "__main__":
    Base.metadata.create_all(engine)

