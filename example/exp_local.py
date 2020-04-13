

from flyannoy import FlyAnnoy
from flyannoy.storage import S3Storage, LocalStorage
from flask import Flask


flyannoy = FlyAnnoy(url_prefix="/api/annoy", vector_length=3)

app = Flask(__name__)
app.register_blueprint(flyannoy)

app.run(debug=True)
