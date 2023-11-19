### Steps to Install/Run Flask

#### Instructions from example here: [Building a Simple REST API with Python and Flask](https://medium.com/@onejohi/building-a-simple-rest-api-with-python-and-flask-b404371dc699)

1. Set up the environment in `src/sandbox` directory:
   md sandbox
   cd .\sandbox\
   py -m venv venv


2.  Activate the env
    Windows: cmd .\src\sandbox\venv\Scripts\> activate
    Mac: ./venv/Scripts/ 
    Linux: venv/bin/activate

3. set env variables:
    Mac:
    $ export FLASK_ENV=development
    $ export FLASK_APP=app.py
    Windows:
    set FLASK_ENV=development
    set FLASK_APP=app.py

4. 
    Then type 'flask run' in your terminal to start running and developing the application.
    sample url: http://127.0.0.1:5000/api/weather?station_id=USC00339312&date=2012-07-01
