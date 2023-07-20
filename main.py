from singleton import ModelSingleton
from keras.models import load_model


try:
    data = load_model('facenet_keras.h5')
    print('valid')
except ValueError:
    print('invalid')
