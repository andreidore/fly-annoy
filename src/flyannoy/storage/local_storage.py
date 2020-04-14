
import json
import os
import shutil

from annoy import AnnoyIndex

from .storage import Storage


class LocalStorage(Storage):

    def __init__(self, path: str = "temp/index"):
        super().__init__()

        self.path = path
        self.vector_path = os.path.join(self.path, "vector")
        self.metadata_path = os.path.join(self.path, "metadata")
        self.index_path = os.path.join(self.path, "index.ann")
        self.reverse_index_path = os.path.join(self.path, "reverse_index.json")

        os.makedirs(self.metadata_path, exist_ok=True)
        os.makedirs(self.vector_path, exist_ok=True)

    def save(self, id: str, vector: list, metadata: dict = {}):

        with open(os.path.join(self.vector_path, id+".json"), "w") as fp:
            json.dump(vector, fp, indent=4, sort_keys=True)

        with open(os.path.join(self.metadata_path, id+".json"), "w") as fp:
            json.dump(metadata, fp, indent=4, sort_keys=True)

    def delete(self, id: str):

        os.remove(os.path.join(self.vector_path, id+".json"))
        os.remove(os.path.join(self.metadata_path, id+".json"))

    def vector_generator(self):

        files = os.listdir(self.vector_path)
        files = [os.path.join(self.vector_path, f) for f in files]
        files.sort()

        for f in files:
            with open(f) as fp:
                yield json.load(fp), f.split("/")[-1].split(".")[0]

    def save_index(self, index_path: str, reverse_index_path: str):
        shutil.copyfile(index_path, self.index_path)
        shutil.copyfile(reverse_index_path, self.reverse_index_path)

    def get_local_index_path(self):
        return self.index_path, self.reverse_index_path
