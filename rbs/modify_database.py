from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from database import Event, Image, Base
from datetime import datetime, timedelta
from os import listdir
from os.path import isdir
import subprocess

IGNORED_DIRS = ['deco_images',]

def add_events(s):
    def commit_or_not(event):
        print(event)
        answer = input("Save? (y/n) ")
        if len(answer) == 0:
            answer = "0"
        is_good = answer[0].lower()
        if is_good == "y":
            s.add(event)
            s.commit()
            print("Event saved")
        elif is_good == "n":
            print("Event not saved")
        else:
            commit_or_not(event)
    while True:
        name = input("name (leave blank if finished): ")
        if name == '':
            break
        venue = input("venue: ")
        year = input("year (4 digit): ")
        month = input("month (2 digit): ").zfill(2)
        day = input("date (2 digit): ").zfill(2)
        time_start = input("time to start (formatted, like '10:00am'): ")
        time_end = input("time to end (formatted, like '4:00 pm'): ")
        is_two_days = input("Is this a two day show? (y/N): ")
        if len(is_two_days) == 0:
            is_two_days = "n"
        if is_two_days[0].lower() == "y":
            days = 2
            show_date = datetime.strptime(f"{day}-{month}-{year}", "%d-%m-%Y")
            show_date2 = show_date + timedelta(days=1)
            month2 = str(show_date2.month).zfill(2)
            day2 = str(show_date2.day).zfill(2)
            time_start2 = input("time to start 2nd day (formatted, like '10:00am'): ")
            time_end2 = input("time to end 2nd day (formatted, like '4:00 pm'): ")
        else:
            days = 1
            month2 = "none"
            day2 = "none"
            time_start2 = "none"
            time_end2 = "none"
        street_number = input("street number: ")
        street_name = input("street name: ")
        city = input("city: ")
        details = input("details (parking, entrance fee, we will be outdoors/indoors...): ")
        new_event = Event(name=name, venue=venue, days=days, 
                            year=year,
                            month=month, day=day,
                            time_start=time_start, time_end=time_end,
                            month2=month2, day2=day2,
                            time_start2=time_start2, time_end2=time_end2,
                            street_name=street_name,
                            street_number=street_number,
                            city=city,
                            details=details)
        commit_or_not(new_event)
        print()


def add_new_images():
    def commit_or_not(image):
        print(image)
        answer = input("Save? (y/n) ")
        if len(answer) == 0:
            answer="0"
        is_good = answer[0].lower()
        if is_good == "y":
            s.add(image)
            s.commit()
            print("Image info saved")
        elif is_good == "n":
            print("Image not saved to database. Run again to add.")
        else:
            commit_or_not(image)
    dir_list = [x for x in listdir('static') if isdir(f'static/{x}') and not x in IGNORED_DIRS]
    print("directoyr list:", dir_list)
    for d in dir_list:
        for i in listdir(f"static/{d}"):
            if not isdir(f'static/{d}/{i}'):
                try:
                    #TODO recall/create object first, then edit 
                    img = s.query(Image).filter(Image.file_name == i, 
                            Image.file_loc == f'static/{d}').one()
                    print(img)
                    answer = input(f"{i} already has entry. Erase and change later? (y/n) ")
                    if len(answer) == 0:
                        answer = "n"
                    else:
                        answer = answer[0].lower()
                    if answer == "y":
                        s.delete(img)
                        s.commit()
                except NoResultFound:
                    print(i, "will have it's entry edited")
                    viewer = subprocess.run(['feh', f'static/{d}/{i}'])
                    image_name = input("Name of image: ")
                    file_loc = f'static/{d}'
                    description = input("Description (optional): ")
                    price = input("Price: ")
                    sold_raw = input("Already sold? (T/F; blank for F): ")
                    if len(sold_raw) == 0:
                        sold_raw = "f"
                    if (sold_raw[0].lower()) == "t":
                        sold = True
                    else:
                        sold = False
                    img = Image(file_name=i,file_loc=file_loc,
                        image_name=image_name,
                        description=description,price=price,sold=sold)
                    commit_or_not(img)
                except MultipleResultsFound:
                    print(i, "Multiples found. Removing all but one")
                    imgs = s.query(Image).filter(Image.file_name == i, 
                            Image.file_loc == f'static/{d}').all()
                    for img in imgs[:-1]:
                        s.delete(img)
                    s.commit()

def edit_image(s):
    print("not yet implemented")

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
        add_new_images()
    if selection == "3":
        edit_image(s=s)

