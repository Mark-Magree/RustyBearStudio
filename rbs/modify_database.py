from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database import Event, Image, Base
from os import listdir
from os.path import isdir

def add_events(s):
    while True:
        name = input("name (leave blank if finished): ")
        if name == '':
            break
        year = input("year (2 digit): ")
        month = input("month (2 digit): ")
        day = input("date (2 digit): ")
        street_name = input("street name: ")
        street_number = input("street number: ")
        city = input("city: ")
        new_event = Event(name=name,year=year,month=month,day=day,
                            street_name=street_name,
                            street_number=street_number,city=city)
        s.add(new_event)
        s.commit()

def add_new_images(s):
    dir_list = [x for x in listdir('static') if isdir(f'static/{x}')]
    print("directoyr list:", dir_list)
    for d in dir_list:
        for i in listdir(f"static/{d}"):
            print(i, "will have it's entry edidted <<test>>")

def edit_image(s):
    pass

if __name__ == "__main__":
    engine = create_engine('sqlite:///rbs.db')
    Session = sessionmaker(bind=engine)
    s = Session()

    print("""What to do?
            1:Add events
            2:Add new images to database
            3:Edit specific image info""")
    selection = input("Choice: ")

    if selection == "1":
        add_events(s=s)
    if selection == "2":
        add_new_images(s=s)
    if selection == "3":
        edit_image(s=s)

