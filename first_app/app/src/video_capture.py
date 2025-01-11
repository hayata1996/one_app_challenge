import cv2 as cv


class VideoCapture:
    def __init__(self, device, width, height):
        self.cap = cv.VideoCapture(device)
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, height)

    def read(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        return cv.flip(frame, 1)

    def release(self):
        self.cap.release()