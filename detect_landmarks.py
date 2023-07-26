import cv2
import tensorflow as tf
import numpy as np
from numpy import asarray
from PIL import Image
from singleton import ModelSingleton
from utility import l2_normalizer, load_pickle
from scipy.spatial.distance import euclidean


def detect_face(face_data):
    models = ModelSingleton.get_instance('facenet_keras.h5')
    img_array = np.array(face_data)
    return models.model.predict(tf.expand_dims(img_array, axis=0))[0]


model = ModelSingleton.get_instance('facenet_keras.h5')

encoding_dict = load_pickle('encodings/encodings.pkl')

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

distance_threshold = 2.5

# Nombre d'images successives pour la détection de mouvement
nb_images = 10
motion_frames = []

cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    for (x1, y1, width, height) in faces:
        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + width, y1 + height

        gbr = Image.fromarray(frame)
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
            dist_norm = euclidean(db_encode, face_signature)
            if dist_norm < dist_norm_min:
                name = db_name
                dist_norm_min = dist_norm

        # Vérifier si le visage est authentique (liveness detection)
        if dist_norm_min < distance_threshold:
            motion_frames.append(gray[y1:y2, x1:x2])

            # Limiter le nombre d'images pour la détection de mouvement
            if len(motion_frames) > nb_images:
                motion_frames.pop(0)

            # Vérifier la différence de mouvement entre les images successives
            motion_diff = np.mean(np.std(np.array(motion_frames), axis=0))
            if motion_diff > 2.0:  # Vous pouvez ajuster cette valeur selon vos besoins
                # Il y a un mouvement suffisant (visage réel)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, name, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                # Mouvement insuffisant (probablement une image statique, faux visage)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, 'Fake Face', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('Anti-Spoofing', frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
