
from .storage import Storage


class S3Storage(Storage):

    def __init__(self):
        super().__init__()

    def save(self, id: str, vector: list, metadata: dict = {}):
        print("S3", id)
