
import json
import os
import shutil
import tempfile
import time

from annoy import AnnoyIndex
from flask import Blueprint, jsonify, make_response, request

from .storage import LocalStorage


class FlyAnnoy(Blueprint):

    def __init__(self, url_prefix="/flyannoy", vector_length=1024, storage=LocalStorage()):
        super().__init__('flyannoy', __name__, url_prefix=url_prefix)

        self.vector_length = vector_length
        self.storage = storage

        self._load_index()

        self.add_url_rule("/add", "add", self.add_vector, methods=["POST"])
        self.add_url_rule("/delete", "delete",
                          self.delete_vector, methods=["POST"])
        self.add_url_rule("/refresh", "refresh",
                          self.refresh, methods=["POST"])
        self.add_url_rule("/search", "search",
                          self.search_vector, methods=["POST"])

    def add_vector(self):

        start_time = time.time()

        request_data = request.get_json()

        id = request_data.get("id")
        if id is None:
            return _create_response("No id in request", status_code=400)

        vector = request_data.get("vector")
        if vector is None:
            return _create_response("No vector in request", status_code=400)

        metadata = request_data.get("metadata", {})

        self.storage.save(id, vector, metadata)

        end_time = time.time()
        duration = end_time-start_time

        response_data = {"id": id, "duration": duration}
        return self._create_response("Ok", 200, response_data)

    def search_vector(self):

        start_time = time.time()

        request_data = request.get_json()

        vector = request_data.get("vector")
        if vector is None:
            return _create_response("No vector in request", status_code=400)

        r = self.index.get_nns_by_vector(
            vector, 10, include_distances=True)

        result = []
        for idx, distance in zip(r[0], r[1]):
            result.append(
                {"distance": distance, "id": self.reverse_index[idx]})

        end_time = time.time()
        duration = end_time-start_time

        response_data = {"duration": duration, "result": result}
        return self._create_response("Ok", 200, response_data)

    def delete_vector(self):

        start_time = time.time()

        request_data = request.get_json()

        id = request_data.get("id")
        if id is None:
            return _create_response("No id in request", status_code=400)

        self.storage.delete(id)

        end_time = time.time()
        duration = end_time-start_time

        response_data = {"id": id, "duration": duration}
        return self._create_response("Ok", 200, response_data)

    def refresh(self):

        start_time = time.time()

        with tempfile.TemporaryDirectory() as temp_folder:

            index_path = os.path.join(temp_folder, "index.ann")
            reverse_index_path = os.path.join(
                temp_folder, "reverse_index.json")

            temp_index = AnnoyIndex(self.vector_length, 'angular')

            temp_reverse_index = []
            i = 0
            for v, id in self.storage.vector_generator():
                temp_index.add_item(i, v)
                temp_reverse_index.append(id)
                i += 1

            temp_index.build(10)
            temp_index.save(index_path)

            with open(reverse_index_path, "w") as fp:
                json.dump(temp_reverse_index, fp, indent=4, sort_keys=True)

            self.storage.save_index(index_path, reverse_index_path)

        self._load_index()

        end_time = time.time()
        duration = end_time-start_time

        response_data = {"duration": duration}
        return self._create_response("Ok", 200, response_data)

    def _create_response(self, message: str, status_code: int, data: dict):

        response_data = {"message": message,
                         "status_code": status_code}

        if data is not None:
            response_data.update(data)

        return make_response(jsonify(response_data), status_code)

    def _load_index(self):

        index_path, reverse_index_path = self.storage.get_local_index_path()

        if not os.path.exists(index_path):
            return

        self.index = AnnoyIndex(self.vector_length, 'angular')
        self.index.load(index_path)

        with open(reverse_index_path) as fp:
            self.reverse_index = json.load(fp)
