import schedule
from flask import Flask
from schedule import every, repeat
from class_camera_recognition import FaceRecognition

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route('/camera')
@repeat(every().day.at('11:50'))
def camera():
    create_instance_01 = FaceRecognition('encodings/encodings.pkl', 10)
    create_instance_01.open_camera_app()
    return 'opened camera'


if __name__ == "__main__":
    app.run(debug=True)
