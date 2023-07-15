import cv2
import tensorflow as tf
import numpy as np
from numpy import asarray
from PIL import Image
from singleton import ModelSingleton
from utility import get_encode, l2_normalizer, load_pickle
from scipy.spatial.distance import cosine


def detect_face(data_face):
    model = ModelSingleton.get_instance()
    img_array = np.array(face)
    return model.model.predict(tf.expand_dims(img_array, axis=0))[0]


face_encoder = ModelSingleton.get_instance('facenet_keras.h5')
required_size = (160, 160)
recognition_t = 0.8,
encoding_dict = load_pickle('encodings/encodings.pkl')
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) > 0:
        x1, y1, width, height = faces[0]
    else:
        # x1, y1, width, height = 1, 1, 10, 10
        continue

    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height

    gbr = cv2.cvtColor(gray, cv2.COLOR_BGR2RGB)
    gbr = Image.fromarray(gbr)  # conversion OpenCV ho PIL
    gbr_array = asarray(gbr)

    face = gbr_array[y1:y2, x1:x2]

    face = Image.fromarray(face)
    face = face.resize((160, 160))
    face = asarray(face)

    face = face.astype('float32')
    mean, std = face.mean(), face.std()
    face = (face - mean) / std

    face_signature = detect_face(face)
    encode = get_encode(face_encoder, face, required_size)
    encode = l2_normalizer.transform(encode.reshape(1, -1))[0]

    name = 'unknown'

    distance = float("inf")
    for db_name, db_encode in encoding_dict.items():
        dist = cosine(db_encode, encode)
        if dist < recognition_t and dist < distance:
            name = db_name
            distance = dist
    if name == 'unknown':
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.putText(frame, name, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
    else:
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, name, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
    # cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

    cv2.imshow('frame', frame)
    if cv2.waitKey(20) & 0XFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
