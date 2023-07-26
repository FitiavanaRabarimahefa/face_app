from pymongo import MongoClient


def handle_database(name, time):
    client = MongoClient('localhost', 27017)
    db = client['face_app']
    student_collection = db['student']
    new_student = {
        'name': name,
        'time_arrived': time,
    }
    result = student_collection.insert_one(new_student)
    if result:
        print('insert successfull')
    else:
        print('error on insert data')
    return result
