

class Storage:

    def save(self, id: str, vector: list, metadata: dict = {}):
        raise ("Not implemented")

    def delete(self, id: str):
        raise ("Not implemented")

    def vector_generator(self):
        raise ("Not implemented")
