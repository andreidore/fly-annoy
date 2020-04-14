# FlyAnnoy


A simple server around [Annoy](https://github.com/spotify/annoy) (K-NN). You can add, delete and search vectors. 

## Install

```sh
pip install git+https://github.com/andreidore/flyannoy
```


## Python code example

```python
from flyannoy import FlyAnnoy
from flask import Flask


flyannoy = FlyAnnoy(url_prefix="/api/annoy", vector_length=3)

app = Flask(__name__)
app.register_blueprint(flyannoy)

app.run(debug=True)

```

## Methods

### Add vector

Add vector to index. 

Mandatory fields:

* id - id of the vector. Must be an unique string. 
* vector - list of number

Optional fields:

* metdata - metadata

```sh
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"id":"1","vector":[1.2,3.4,5.6]}' \
  http://localhost:5000/api/annoy/add
```

### Delete vector

Delete vector from index. 

Mandatory fields:

* id - id of the vector.

Delete vector
```sh
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"id":"1"}' \
  http://localhost:5000/api/annoy/delete
```


Search vector
```sh
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"vector":[1,2,3]}' \
  http://localhost:5000/api/annoy/search
```

Refresh index
```
curl --header "Content-Type: application/json" \
  --request POST \
  http://localhost:5000/api/annoy/refresh
```

## Storage 

FlyAnnoy support a plugable storage for vectors and index.

### Local Storage

Local storage store the vector in separate files in local file system. 


### S3 Storage

You can store vectors, metadata and index in S3

```python
from flyannoy import FlyAnnoy,S3Storage
from flask import Flask


flyannoy = FlyAnnoy(url_prefix="/api/annoy", vector_length=3,storage=S3Storage("bucket","key","local_path")

app = Flask(__name__)
app.register_blueprint(flyannoy)

app.run(debug=True)
```

