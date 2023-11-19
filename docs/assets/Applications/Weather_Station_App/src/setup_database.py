from sqlalchemy import create_engine
from models import Base, WeatherData, StationStats

engine = create_engine('sqlite:///weather_data.db')

Base.metadata.create_all(engine)
db_connection = engine.connect()