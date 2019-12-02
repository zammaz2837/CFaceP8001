from abc import ABC, abstractmethod

from src.face_recognition.calc_embedding.calculator import calculate_embeddings
from src.face_recognition.classify_embedding.predict import predict_from_image_with_classifier
from src.face_recognition.classify_embedding.train import get_trained_classifier
from src.face_recognition.crop_faces.crop_faces import crop_one_face
from test_perf.dto import Image, Name


class ModelWrapperBase(ABC):
    @abstractmethod
    def add_example(self, img: Image, name: Name):
        pass

    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def recognize(self, img: Image):
        pass


class PythonModel(ModelWrapperBase):
    def __init__(self):
        self._cropped_images = []
        self._names = []
        self._classifier = None

    def add_example(self, img: Image, name: Name):
        cropped_img = crop_one_face(img)
        self._cropped_images.append(cropped_img)
        self._names.append(name)

    def train(self):
        embeddings = calculate_embeddings(self._cropped_images)
        self._classifier = get_trained_classifier(embeddings, self._names)

    def recognize(self, img: Image):
        return predict_from_image_with_classifier(img=img, classifier=self._classifier, limit=1)


class RESTAPIModel(ModelWrapperBase):
    def add_example(self, img: Image, name: Name):
        pass

    def train(self):
        pass

    def recognize(self, img: Image):
        pass
