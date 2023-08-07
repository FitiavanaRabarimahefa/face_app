from pymongo import MongoClient
import datetime


def create_connexion():
    client = MongoClient('localhost', 27017)
    db = client['face_app']
    return db


def compare_time(name):
    time = datetime.datetime.now()
    time_arrived = time.strftime("%H:%M:%S")
    time_default = "08:21:00"

    if time_arrived < time_default:
        presence_status = True
        insert_student(name, time_arrived, presence_status)
    else:
        presence_status = "retard"
        insert_student(name, time_arrived, presence_status)


def insert_student(name, time, status):
    db = create_connexion()
    student_collection = db['student']
    new_student = {
        'name': name,
        'time_arrived': time,
        'presence_status': status
    }
    result = student_collection.insert_one(new_student)
    if result:
        print('insert successfull')
    else:
        print('error on insert data')
    return result


def check_insert(name):
    db = create_connexion()
    student_collection = db['student']
    if student_collection.count_documents({"name": name}) != 0:
        print("always in database")
    else:
        compare_time(name)


def add_schedule_database(subject, date, start_time, end_time, semester):
    db = create_connexion()
    schedule_collection = db['schedule']
    schedule_data = {
        'subject': subject,
        'date': date,
        'start_time': start_time,
        'end_time': end_time,
        'semester': semester
    }
    result = schedule_collection.insert_one(schedule_data)
    if result:
        print('insert schedule successfull')
    else:
        print('error on insert schedule data')
    return result
