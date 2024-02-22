import cv2


class Detector:
    def __init__(self, path):
        self.model = cv2.CascadeClassifier(path)

    def detect(self, fp) -> bool:
        image = cv2.imread(fp)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return bool(self.model.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5,
                                                minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE))
