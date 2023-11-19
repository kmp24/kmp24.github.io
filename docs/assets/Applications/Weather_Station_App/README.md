# Code Challenge Template
### Introduction
#### This code ingests all of the txt files in wx_data (Monthly weather station records for numerous years) and places them in an SQLite database for further analysis. 
#### This analysis is the basis of a flask application that generates an json endpoint.

### Instructions
Install requirements:
>   pip install -r requirements.txt

Running main.py runs the following steps:
>   1. run concat_data.py. This concatenates all the .txt weather station data files.
>   2. run data_model.py, which only needs to be run once if the weather_data.db does not already exist.
>   3. run ingest_data.py, which takes the processed weather data and puts it in the weather_data table.
>   4. run aggregate_station_data.py, which takes the data from the database and generates mean max/min, total precipitation, for each station and year.

 The flask app setup instructions are located in the README here: code-challenge-template\src\sandbox

### Notes
All table ORM is contained in data_model.py. Some constants are stored in constants.py for easy modification.
