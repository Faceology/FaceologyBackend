# FaceologyBackend
This repository contains the backend for the Faceology mobile app along with experiments.

Faceology's backend is hosted on an AmazonEC2 instance, but the REST API can also be deployed locally.

Although there is no requirements.txt file present, the REST server in this repository needs python3 to run (namely for the use of face_recognition)

Additionally, the following dependencies must be installed via pip3:
* face_recognition
* PIL
* Flask
* Flask-RESTful
* psycopg2
* requests
* SQLAlchemy
* numpy

Additionally, a PSQL database needs to be created and initialized using the create_db.sql. To do this on Linux, one can run the following commands:

`sudo yum install postgresql postgresql-server postgresql-devel postgresql-contrib postgresql-docs`

`sudo service postgresql initdb`

`sudo service postgresql start`

And after creating a DB in PSQL, run:

`psql -U your_user -d your_db -f create_db.sql`

Once dependencies are installed and the database is setup, the server can be ran with:

`python3 routes.py`
