import cv2
import tensorflow as tf
import numpy as np
import datetime
from numpy import asarray
from PIL import Image
from singleton import ModelSingleton
from utility import l2_normalizer, load_pickle
from scipy.spatial.distance import euclidean
from database_connection import handle_database


def detect_face(face_data):
    model = ModelSingleton.get_instance('facenet_keras.h5')
    img_array = np.array(face_data)
    return model.model.predict(tf.expand_dims(img_array, axis=0))[0]


recognition_t = 0.07,
encoding_dict = load_pickle('encodings/encodings.pkl')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(1)
while True:
    time = datetime.datetime.now()
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    if len(faces) == 0:
        continue

    for (x1, y1, width, height) in faces:
        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + width, y1 + height

        gbr = Image.fromarray(frame)  # conversion OpenCV ho PIL
        gbr_array = asarray(gbr)

        face = gbr_array[y1:y2, x1:x2]

        face = Image.fromarray(face)
        face = face.resize((160, 160))
        face = asarray(face)

        face = face.astype('float32')
        mean, std = face.mean(), face.std()
        face = (face - mean) / std
        face_signature = detect_face(face)
        encode = l2_normalizer.transform(face_signature.reshape(1, -1))[0]

        name = 'unknown'
        dist_norm_min = 100
        distance = float("inf")
        for db_name, db_encode in encoding_dict.items():
            # dist_norm = np.linalg.norm(db_encode - face_signature)
            dist_norm = euclidean(db_encode, face_signature)
            if dist_norm < dist_norm_min and dist_norm < 2.6:
                name = db_name
                dist_norm_min = dist_norm
                print(dist_norm_min)

        if name == 'unknown':
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(frame, name, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
        else:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, name, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
            # handle_database(name, time)
            print(time)
    cv2.imshow('frame', frame)
    if cv2.waitKey(20) & 0XFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
