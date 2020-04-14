
import io
import os
import json
import subprocess
import shutil

import boto3

from .storage import Storage


class S3Storage(Storage):

    def __init__(self, bucket: str, key: str, local_path: str):
        super().__init__()
        self.bucket = bucket
        self.key = key

        self.index_key = key+"/index"
        self.annoy_index_key = self.index_key+"/index.ann"
        self.reverse_index_key = self.index_key+"/reverse_index.json"

        self.vector_key = key+"/vector"
        self.metadata_key = key+"/metadata"

        self.local_index_path = local_path+"/index"
        self.local_annoy_index_path = self.local_index_path+"/index.ann"
        self.local_reverse_index_path = self.local_index_path+"/reverse_index.json"
        self.local_vector_path = local_path+"/vector"

        self.s3_client = boto3.client("s3")

    def save(self, id: str, vector: list, metadata: dict = {}):

        vector_key = self.vector_key+"/"+id+".json"
        self.s3_client.upload_fileobj(io.BytesIO(json.dumps(vector, indent=4, sort_keys=True).encode("utf-8")),
                                      self.bucket, vector_key)

        metadata_key = self.metadata_key+"/"+id+".json"
        self.s3_client.upload_fileobj(io.BytesIO(json.dumps(metadata, indent=4, sort_keys=True).encode("utf-8")),
                                      self.bucket, metadata_key)

    def delete(self, id: str):

        pass

    def vector_generator(self):

        remote_path = "s3://"+self.bucket+"/"+self.vector_key

        subprocess.call(["aws", "s3", "sync", remote_path,
                         self.local_vector_path, "--delete"])

        files = os.listdir(self.local_vector_path)
        files = [os.path.join(self.local_vector_path, f) for f in files]
        files.sort()

        for f in files:
            with open(f) as fp:
                yield json.load(fp), f.split("/")[-1].split(".")[0]

    def save_index(self, index_path: str, reverse_index_path: str):

        self.s3_client.upload_file(
            index_path, self.bucket, self.annoy_index_key)
        self.s3_client.upload_file(
            reverse_index_path, self.bucket, self.reverse_index_key)

    def get_local_index_path(self):

        index_remote_path = "s3://"+self.bucket+"/"+self.index_key
        subprocess.call(["aws", "s3", "sync", index_remote_path,
                         self.local_index_path, "--delete"])

        return self.local_annoy_index_path, self.local_reverse_index_path
