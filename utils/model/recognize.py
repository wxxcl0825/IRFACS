import os

import numpy as np
from tqdm import tqdm
import logging
from typing import Any, List, Dict

import cv2
from numpy import ndarray, dtype
from utils.paths import *
import face_recognition as fr
import pickle


class Recognizer:
    model: Dict[int, List[ndarray[Any, dtype]]]

    def __init__(self, path):
        self.model_path = path
        self.model = {}
        try:
            self.model = pickle.load(open(self.model_path, 'rb'))
            logging.info("MODEL: Successfully load.")

        except FileNotFoundError:
            logging.warning("MODEL: File not found.")
            self.train()

        except pickle.PickleError:
            logging.warning("MODEL: File corrupted.")
            os.remove(self.model_path)
            self.train()

    def train(self):
        users = os.listdir(PATH_TEMPLATE_DIR)
        logging.info("MODEL: Training...")
        for user in tqdm(users):
            self.insert(uid=int(user.split('.')[0]), fp=os.path.join(PATH_TEMPLATE_DIR, user))
        self.save()

    def save(self):
        pickle.dump(self.model, open(self.model_path, 'wb'))

    def insert(self, uid: int, fp):
        image = cv2.imread(fp)
        self.model[uid] = fr.face_encodings(image, fr.face_locations(image))[0]

    def delete(self, uid: int):
        if uid in self.model:
            del self.model[uid]

    def predict(self, fp) -> None | int:
        # stranger -> -1
        try:
            image = cv2.imread(fp)
            assert image is not None
            obj_enc = fr.face_encodings(image, fr.face_locations(image))
            if not obj_enc:
                return None
            uids, encodings = list(self.model.keys()), list(self.model.values())
            dis = fr.face_distance(encodings, obj_enc[0])
            pos = np.argmin(dis)
            if dis[pos] > 0.4:
                return -1
            return uids[pos]

        except AssertionError:
            logging.error("MODEL: Invalid image. Abort.")
            return None
