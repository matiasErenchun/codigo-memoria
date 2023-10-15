import os
import cv2
import threading


class camThread(threading.Thread):

    def __init__(self, previewName, camID):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID

    def run(self):
        print("Starting " + self.previewName)
        camPreview(self.previewName, self.camID)


def camPreview(previewName, camID):
    cv2.namedWindow(previewName)
    cam = cv2.VideoCapture(camID)
    cam.set(cv2.CAP_PROP_FPS, 15)
    if cam.isOpened():  # try to get the first frame
        rval, frame = cam.read()
    else:
        rval = False

    while rval:
        cv2.imshow(previewName, frame)
        rval, frame = cam.read()
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    cv2.destroyWindow(previewName)


def contar_camaras():
    num_cameras = 0
    while True:
        try:
            cap = cv2.VideoCapture(num_cameras)
            if not cap.read()[0]:
                break
        except Exception:
            print("si")
            break

        num_cameras += 1
        cap.release()
    return num_cameras


if __name__ == '__main__':
    print("hola")
    num_camaras = contar_camaras()
    list_thread = []
    for i in range(num_camaras):
        thread = camThread("camera "+str(i), i)
        list_thread.append(thread)

    for j in range(num_camaras):
        list_thread[j].start()
