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
                "INF101": random.randint(5, 20),
                "INF104": random.randint(5, 20),
                "INF107": random.randint(5, 20),
                "MTH101": random.randint(5, 20),
                "MTH102": random.randint(5, 20),
                "ORG101": random.randint(5, 20),
                "Nb_retard": random.randint(5, 20),
                "Nb_absence": random.randint(5, 20),
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


def fake_data_mention_prediction():
    tab_data_fake = []
    for x in range(1, 150):
        data_fake = {
            "Semestre_1": {
                "INF101": random.randint(7, 20),
                "INF104": random.randint(7, 20),
                "INF107": random.randint(7, 20),
                "MTH101": random.randint(7, 20),
                "MTH102": random.randint(7, 20),
                "ORG101": random.randint(7, 20),
            },
            "Semestre_2": {
                "INF102": random.randint(7, 20),
                "INF103": random.randint(7, 20),
                "INF105": random.randint(7, 20),
                "MTH106": random.randint(7, 20),
                "MTH103": random.randint(7, 20),
                "MTH105": random.randint(7, 20),
            },
            "Semestre_3": {
                "INF201": random.randint(7, 20),
                "INF202": random.randint(7, 20),
                "INF203": random.randint(7, 20),
                "INF208": random.randint(7, 20),
                "MTH201": random.randint(7, 20),
                "ORG201": random.randint(7, 20),
            },
        }
        tab_data_fake.append(data_fake)
        with open("dataset_mention_predict.json", "w") as f:
            json.dump(tab_data_fake, f)
    return tab_data_fake


def combination_data(data):
    combined_data = {}
    for semester_data in data:
        for semester, subjects in semester_data.items():
            if semester not in combined_data:
                combined_data[semester] = subjects
            else:
                combined_data[semester].update(subjects)
    return combined_data


def get_all_good_mark_semester():
    with open('dataset_mention_predict.json') as f:
        data = json.load(f)
    data_tmp = combination_data(data)

    marks_superior = []
    for semester, subjects in data_tmp.items():
        marks_superior_subjects = {}
        for subject, mark in subjects.items():
            if mark > 10:
                marks_superior_subjects[subject] = mark
        if marks_superior_subjects:
            marks_superior.append({semester: marks_superior_subjects})

    return marks_superior


def checking_dev(data):
    for student in data:
        marks_s1 = [student["Semestre_1"]["INF101"],
                    student["Semestre_1"]["INF104"],
                    student["Semestre_1"]["INF107"],
                    student["Semestre_1"]["MTH102"]]
        marks_s2 = [
            student["Semestre_2"]["INF102"],
            student["Semestre_2"]["INF105"],
            student["Semestre_2"]["MTH103"]
        ]
        marks_s3 = [
            student["Semestre_3"]["INF201"],
            student["Semestre_3"]["INF202"],
            student["Semestre_3"]["INF208"]
        ]

        semester_1 = sum(marks_s1) / len(marks_s1)
        semester_2 = sum(marks_s2) / len(marks_s2)
        semester_3 = sum(marks_s3) / len(marks_s3)
        report_marks = (semester_1 + semester_2 + semester_3) / 3
        return report_marks


def checking_data_mention(data):
    for student in data:
        marks_s1 = [student["Semestre_1"]["MTH101"],
                    student["Semestre_1"]["MTH102"],
                    student["Semestre_1"]["INF107"],
                    ]
        marks_s2 = [
            student["Semestre_2"]["INF102"],
            student["Semestre_2"]["INF103"],
            student["Semestre_2"]["INF105"],
            student["Semestre_2"]["MTH105"]
        ]
        marks_s3 = [
            student["Semestre_3"]["INF202"],
            student["Semestre_3"]["INF203"],
            student["Semestre_3"]["INF208"],
            student["Semestre_3"]["ORG201"],
        ]

        semester_1 = sum(marks_s1) / len(marks_s1)
        semester_2 = sum(marks_s2) / len(marks_s2)
        semester_3 = sum(marks_s3) / len(marks_s3)
        report_marks = (semester_1 + semester_2 + semester_3) / 3
        return report_marks


def checking_web_design(data):
    for student in data:
        marks_s1 = [student["Semestre_1"]["INF101"],
                    student["Semestre_1"]["INF104"],
                    student["Semestre_1"]["INF107"],
                    ]
        marks_s2 = [
            student["Semestre_2"]["INF105"],
        ]
        marks_s3 = [
            student["Semestre_3"]["INF201"],
            student["Semestre_3"]["MTH201"],
        ]

        semester_1 = sum(marks_s1) / len(marks_s1)
        semester_2 = sum(marks_s2) / len(marks_s2)
        semester_3 = sum(marks_s3) / len(marks_s3)
        report_marks = (semester_1 + semester_2 + semester_3) / 3
        return report_marks


def create_mention_data():
    with open('dataset_mention_predict.json') as f:
        data = json.load(f)
    tab_max_key = []
    for value in data:
        check_dev = checking_dev([value])
        check_data_mention = checking_data_mention([value])
        check_web_design = checking_web_design([value])

        marks = {
            "dev": check_dev,
            "base de donnée": check_data_mention,
            "web design": check_web_design
        }

        max_key = max(marks, key=lambda k: marks[k])
        value["mention"] = max_key
        tab_max_key.append(max_key)
        with open("dataset_mention_predict.json", "w") as f:
            json.dump(data, f)
    return data


# create_dict_fake_data()
# load_data = add_pt_on_json()
# print(load_data)
# add_pt_on_json()
# fake_data_mention_prediction()
# print(get_all_good_mark_semester())
print(create_mention_data())
# print(test())
