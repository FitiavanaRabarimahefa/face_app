import numpy as np
import cv2
import mtcnn
from scipy.spatial.distance import cosine
from singleton import ModelSingleton
from utility import get_face, l2_normalizer, get_encode, plt_show, load_pickle

face_detector = mtcnn.MTCNN()
face_encoder = ModelSingleton.get_instance('facenet_keras.h5')
encodings_path = 'encodings/encodings.pkl'
img_test_path = 'img_test/mbappe.jfif'
# img_test_result_path = 'img_test_result/messi_neymar.jpeg'

recognition_t = 0.07  # first_test_0.1 second_test_0.06 third_test 0.05 stable_test_0.07
required_size = (160, 160)

encoding_dict = load_pickle(encodings_path)
face_detector = mtcnn.MTCNN()
face_encoder = ModelSingleton.get_instance('facenet_keras.h5')

img = cv2.imread(img_test_path)
# plt_show(img)

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
results = face_detector.detect_faces(img_rgb)
for res in results:
    face, pt_1, pt_2 = get_face(img_rgb, res['box'])
    encode = get_encode(face_encoder, face, required_size)
    encode = l2_normalizer.transform(np.expand_dims(encode, axis=0))[0]

    name = 'unknown'
    distance = float("inf")

    for db_name, db_encode in encoding_dict.items():
        dist = cosine(db_encode, encode)
        if dist < recognition_t and dist < distance:
            name = db_name
            distance = dist
            print('distance', distance)
            print('name', name)
            print(dist)
    if name == 'unknown':
        cv2.rectangle(img, pt_1, pt_2, (0, 0, 255), 2)
        cv2.putText(img, name, pt_1, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
    else:
        cv2.rectangle(img, pt_1, pt_2, (0, 255, 0), 2)
        cv2.putText(img, name, pt_1, cv2.FONT_HERSHEY_PLAIN, 4, (0, 255, 0), 4)

cv2.imwrite('img_test_result/result.jpeg', img)
plt_show(img)
