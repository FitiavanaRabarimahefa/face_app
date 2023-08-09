from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from multiprocessing import Process
from apscheduler.triggers.cron import CronTrigger
from class_camera_recognition import FaceRecognition

app = Flask(__name__)


@app.route('/')
def open_detection():
    create_instance_01 = FaceRecognition('encodings/encodings.pkl', 10)
    create_instance_01.open_camera_app()


scheduler = BackgroundScheduler()
scheduler.add_job(open_detection, trigger='cron', hour='11', minute='10', id='instance01')
scheduler.start()


@app.route('/add_schedule', methods=['GET'])
def add_schedule():
    return 'hello'


if __name__ == "__main__":
    """"
    while True:
        time.sleep(1)
        # Modifiez l'heure du schedule
        scheduler.reschedule_job('instance01', trigger='cron', hour='11', minute='06')
        # scheduler.modify_job('instance01', trigger='cron', hour='18', minute='13')
    """

app.run(debug=True)
