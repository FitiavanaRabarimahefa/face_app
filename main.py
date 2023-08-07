from apscheduler.schedulers.background import BackgroundScheduler
import time
from flask import Flask
from apscheduler.triggers.cron import CronTrigger
from class_camera_recognition import FaceRecognition

app = Flask(__name__)


@app.route('/')
def open_detection():
    create_instance_01 = FaceRecognition('encodings/encodings.pkl', 10)
    create_instance_01.open_camera_app()


scheduler = BackgroundScheduler()
scheduler.add_job(open_detection, trigger='cron', hour='17', minute='48', id='instance01')
scheduler.start()

if __name__ == "__main__":
    while True:
        time.sleep(1)
        # Modifiez l'heure du schedule
        scheduler.reschedule_job('instance01', trigger='cron', hour='05', minute='33')
        # scheduler.modify_job('instance01', trigger='cron', hour='18', minute='13')

app.run(port=5000, debug=True, reload=True)
