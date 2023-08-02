import schedule
import time
from flask import Flask
from schedule import every, repeat
from class_camera_recognition import FaceRecognition

app = Flask(__name__)


@app.route('/')
def open_detection():
    create_instance_01 = FaceRecognition('encodings/encodings.pkl', 10)
    create_instance_01.open_camera_app()


schedule.every().day.at('08:01').do(open_detection)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)

app.run(port=5000, debug=True, reload=True)
