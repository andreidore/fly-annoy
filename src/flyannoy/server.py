import argparse
import os
import sys

from flask import Flask

from flyannoy import FlyAnnoy
from flyannoy.storage import LocalStorage, S3Storage


def main():
    print("Start FlyAnnoy server.")

    parser = argparse.ArgumentParser(
        description='FlyAnnoy - Simple server for Annoy.')
    parser.add_argument("--length", help="Vector length",
                        required=True, type=int)
    parser.add_argument("--storage", help="Storage",
                        choices=["s3", "local"], required=True)

    parser.add_argument("--s3_bucket", help="S3 bucket")
    parser.add_argument("--s3_key", help="S3 key")

    parser.add_argument("--http_port", help="Http port", default=5600)
    parser.add_argument("--http_path", help="Http path", default="/api/annoy")

    args = parser.parse_args()

    if args.storage == "s3":

        if args.s3_bucket is None or args.s3_key is None:

            parser.error(
                "--s3_bucket and --s3_key is required when storage is s3.")

    print("Http port :", args.http_port)
    print("Http path :", args.http_path)
    print("Vector length:", args.length)
    print("Storage :", args.storage)

    if args.storage == "s3":
        print("S3 bucket:", args.s3_bucket)
        print("S3 key :", args.s3_key)

        storage = S3Storage(args.s3_bucket, args.s3_key, "temp/s3")

    else:
        pass

    flyannoy = FlyAnnoy(url_prefix=args.http_path, vector_length=args.length,
                        storage=storage)

    app = Flask(__name__)
    app.register_blueprint(flyannoy)

    app.run(debug=False, port=args.http_port)


if __name__ == "__main__":
    main()
