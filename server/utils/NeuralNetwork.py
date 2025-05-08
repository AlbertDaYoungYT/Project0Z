
from numpy import ndarray
import keras
import os

import loguru

from utils.Errors import Codes


class KerasBased:

    def __init__(self):
        self.train_data: ndarray | None = None
        self.eval_data: ndarray | None = None
        self.model = keras.models.Sequential()

    def _build(self, input_shape=(8,)):
        self.model.add(keras.layers.Dense(12, input_shape=input_shape, activation='relu'))
        self.model.add(keras.layers.Dense(8, activation='relu'))
        self.model.add(keras.layers.Dense(1, activation='sigmoid'))
    
    def _compile(self, loss='binary_crossentropy', optimizer='adam', metrics=["accuracy"]):
        self.model.compile(loss=loss, optimizer=optimizer, metrics=metrics)
    
    def _fit(self, x, y, epochs=150, batch_size=10):
        self.model.fit(x, y, epochs=epochs, batch_size=batch_size)
    
    def __save__(self, filename, force=False) -> Codes.DIRECTORY_EXISTS | bool:
        if os.path.exists(filename) and not force:
            loguru.logger.warning(Codes.DIRECTORY_EXISTS.to_logger())
            return Codes.DIRECTORY_EXISTS

        self.model.save("static/assets/keras/"+filename)
        return True
    
    def __load__(self, filename) -> Codes.FILE_NOT_FOUND | bool:
        if not os.path.exists(filename):
            loguru.logger.warning(Codes.FILE_NOT_FOUND.to_logger())
            return Codes.FILE_NOT_FOUND
        
        self.model = keras.saving.load_model("static/assets/keras/"+filename)
        return True
    
    def predict(self, x):
        return self.model.predict(x)
    
    def train(self) -> float:
        self._fit(self.train_data, self.eval_data)
        _, accuracy = self.model.evaluate(self.train_data, self.eval_data)
        return accuracy