

class Storage:

    def save(self, id: str, vector: list, metadata: dict = {}):
        raise ("Not implemented")

    def delete(self, id: str):
        raise ("Not implemented")

    def vector_generator(self):
        raise ("Not implemented")

    def save_index(self, index_path: str, reverse_index_path: str):
        raise("Not implemented")

    def get_local_index_path(self):
        raise("Not implemented")
