from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database import Event, Base

engine = create_engine('sqlite:///event_info.db')
Session = sessionmaker(bind=engine)
s = Session()

while True:
    name = input("name: ")
    if name == '':
        break
    date = input("date: ")
    street_name = input("street name: ")
    street_number = input("street number: ")
    city = input("city: ")

    new_event = Event(name=name,date=date,street_name=street_name,
                        street_number=street_number,city=city)

    s.add(new_event)
    s.commit()
