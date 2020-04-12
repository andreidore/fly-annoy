# FlyAnnoy



## Python code example

```python
from flyannoy import FlyAnnoy
from flask import Flask


flyannoy = FlyAnnoy(url_prefix="/api/annoy", vector_length=3)

app = Flask(__name__)
app.register_blueprint(flyannoy)

app.run(debug=True)

```


Add vector
```sh
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"id":"1","vector":[1.2,3.4,5.6]}' \
  http://localhost:5000/api/annoy/add
```

Delete vector
```sh
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"id":"1"}' \
  http://localhost:5000/api/annoy/delete
```

Refresh index
```
curl --header "Content-Type: application/json" \
  --request POST \
  http://localhost:5000/api/annoy/refresh
```



