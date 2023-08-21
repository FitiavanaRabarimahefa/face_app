from pymongo import MongoClient
import datetime
import random
import json


def create_connexion():
    client = MongoClient('localhost', 27017)
    db = client['face_app']
    return db


def calculate_time_difference(time_arrived, time_default):
    time_d = datetime.datetime.strptime(time_default, "%H:%M:%S")
    time_arr = datetime.datetime.strptime(time_arrived, "%H:%M:%S")
    difference = time_arr - time_d
    difference_in_minutes = difference.total_seconds() // 60
    return difference_in_minutes


def compare_time(name):
    time = datetime.datetime.now()
    time_arrived = time.strftime("%H:%M:%S")
    time_default = "08:21:00"

    if time_arrived <= time_default:
        presence_status = True
        insert_student(name, time_arrived, presence_status)
    else:
        difference = calculate_time_difference(time_arrived, time_default)
        presence_status = "retard " + str(difference) + " minutes"
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


# add_schedule_database("Math", "20-0.-2023", "09:00:00", "10:00:00", "S1")

def calculate_pt_abandonment(retard, absence, total_hours):
    h_total_missing = retard + absence
    pt_total = (h_total_missing / total_hours) * 100
    return round(pt_total, 2)


def create_dict_fake_data():
    tab_data_fake = []
    for x in range(1, 150):
        data_fake = {
            "Semestre_1": {
                "INF101": random.randint(2, 11),
                "INF104": random.randint(2, 11),
                "INF107": random.randint(2, 11),
                "MTH101": random.randint(2, 11),
                "MTH102": random.randint(2, 11),
                "ORG101": random.randint(2, 11),
                "Nb_retard": random.randint(0, 40),
                "Nb_absence": random.randint(0, 40),

            },
            "Semestre_2": {
                "INF106": random.randint(2, 11),
                "MTH103": random.randint(2, 11),
                "MTH105": random.randint(2, 11),
                "Nb_retard": random.randint(0, 40),
                "Nb_absence": random.randint(0, 40),

            },
            "Semestre_3": {
                "INF201": random.randint(2, 11),
                "INF202": random.randint(2, 11),
                "INF203": random.randint(2, 11),
                "INF208": random.randint(2, 11),
                "MTH201": random.randint(2, 11),
                "ORG201": random.randint(2, 11),
                "Nb_retard": random.randint(0, 40),
                "Nb_absence": random.randint(0, 40),

            },
            "Semestre_4": {
                "INF207": random.randint(2, 11),
                "INF210": random.randint(2, 11),
                "MTH204": random.randint(2, 11),
                "MTH205": random.randint(2, 11),
                "MTH206": random.randint(2, 11),
                "MTH203": random.randint(2, 11),
                "Nb_retard": random.randint(0, 40),
                "Nb_absence": random.randint(0, 40),

            },
            "Semestre_5": {
                "INF301": random.randint(2, 11),
                "INF304": random.randint(2, 11),
                "INF307": random.randint(2, 11),
                "ORG301": random.randint(2, 11),
                "ORG302": random.randint(2, 11),
                "ORG303": random.randint(2, 11),
                "Nb_retard": random.randint(0, 40),
                "Nb_absence": random.randint(0, 40),

            },
            "Semestre_6": {
                "INF310": random.randint(2, 11),
                "ORG304": random.randint(2, 11),
                "Nb_retard": random.randint(0, 40),
                "Nb_absence": random.randint(0, 40),

            },

        }
        tab_data_fake.append(data_fake)
        with open("dataset_with_contraint.json", "w") as f:
            json.dump(tab_data_fake, f)
    return tab_data_fake


def add_pt_on_json():
    with open('dataset_with_contraint.json') as f:
        data = json.load(f)
    for student in data:
        notes = [student["Semestre_1"]["INF101"],
                 student["Semestre_1"]["INF104"],
                 student["Semestre_1"]["INF107"],
                 student["Semestre_1"]["MTH101"],
                 student["Semestre_1"]["MTH102"],
                 student["Semestre_1"]["ORG101"]]
        moyenne = sum(notes) / len(notes)

        if moyenne > 10:
            student["Semestre_1"]["Pb_abandonnement"] = 0
        else:
            student["Semestre_1"]["Pb_abandonnement"] = 1

        with open("dataset_with_contraint.json", "w") as f:
            json.dump(data, f)
    return data


# create_dict_fake_data()
# load_data = add_pt_on_json()
# print(load_data)
add_pt_on_json()
