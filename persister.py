import pickle
from seriesData.library import Library
from tracking.user import User
from genericpath import exists


SAVE_FILE_NAME = "data"


class Persister:
    def __init__(self) -> None:
        self.library = Library()
        self.user = User()


    def save(self):
        with open(SAVE_FILE_NAME, "wb") as fileStream:
            pickle.dump(self, fileStream)
            

    @staticmethod
    def load() -> 'Persister':
        lib = Persister()
        if exists(SAVE_FILE_NAME):
            with open(SAVE_FILE_NAME, "rb") as fileStream:
                lib = pickle.load(fileStream)
        return lib