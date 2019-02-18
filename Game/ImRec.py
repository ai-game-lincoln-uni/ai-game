import cv2
import numpy as np
from matplotlib import pyplot as plt
from time import sleep


def main():

    cap = cv2.VideoCapture(0)

    while True:
        _, frame = cap.read()

        #edges = cv2.Canny(frame, 75, 150)
        #cv2.imshow('edges', edges)

        #overlay = cv2.addWeighted(frame, 0.5, edges, 0.5, 0)
        #cv2.imshow('Overlay', overlay)

        #laplacian = cv2.Laplacian(frame, cv2.CV_64F)
        #cv2.imshow('Laplacian', laplacian)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow('feed', frame)
        cv2.imshow('Greyscale', gray)

        k = cv2.waitKey(5) & 0xFF

        if k == ord('q'):
            break

    cv2.destroyAllWindows()
    cap.release()


def corners():
    cap = cv2.VideoCapture(0)

    while True:
        _, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        gray = np.float32(gray)
        corners = cv2.goodFeaturesToTrack(gray, 500, 0.01, 10)
        corners = np.int0(corners)

        for corner in corners:
            x, y = corner.ravel()
            cv2.circle(frame, (x, y), 3, 255, -1)

        cv2.imshow('feed', frame)
        #cv2.imshow('Greyscale', gray)

        k = cv2.waitKey(5) & 0xFF

        if k == ord('q'):
            break

    cv2.destroyAllWindows()
    cap.release()


def err():
    try:
        cap = cv2.VideoCapture(1)
        _, frame = cap.read()
        cv2.imshow('Image', frame)
        while True:
            k = cv2.waitKey(5) & 0xFF
            if k == ord('q'):
                cv2.destroyAllWindows()
                break
        print("Camera Found")
    except:
        print("ERROR: No camera detected")
    finally:
        print("End")

    cap.release()


def findCams():
    allFound = False
    camera = 0;
    cameras = []
    choice = -1

    while not allFound:
        try:
            cap = cv2.VideoCapture(camera)
            _, frame = cap.read()
            cv2.imshow('Feed', frame)
            cameras.append(camera)
            cap.release()
            print("Camera", camera, "added")
            camera += 1
        except:
            allFound = True
            print("Cameras found")


    # print("Choose Input Feed")
    #
    # while choice == -1:
    #     for feed in cameras:
    #         cap = cv2.VideoCapture(feed)
    #         _,





#main()
#corners()
#err()
findCams()