import cv2
from multiprocessing import Process


def process_1():
    cap = cv2.VideoCapture(1)
    while True:
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(20) & 0XFF == ord('q'):
            break


def process_2():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(20) & 0XFF == ord('f'):
            break


if __name__ == "__main__":
    # Create two processes
    p1 = Process(target=process_1)
    p2 = Process(target=process_2)

    # Start the processes
    p1.start()
    p2.start()

    # Wait for the processes to finish
    p1.join()
    p2.join()
