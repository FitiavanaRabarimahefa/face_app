from singleton import ModelSingleton

try:
    ModelSingleton.get_instance("./facenet_keras.h5")
    print('valid')
except ValueError:
    print('invalid')
