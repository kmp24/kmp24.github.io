from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, Column, Integer, String, Date, Numeric, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base

# Create the data model for the weather station data
Base = declarative_base()

class WeatherData(Base):
    __tablename__ = 'weather_stations'
    station_id = Column(String)
    date= Column('date', Date)
    max_temp_tenths_c = Column('max_temp_tenths_c', Integer)
    min_temp_tenths_c = Column('min_temp_tenths_c', Integer)
    precip_tenths_mm = Column('precip_tenths_mm', Integer)
    
    # Create a composite primary key since station_id is not unique
    __table_args__ = (
        PrimaryKeyConstraint('station_id', 'date'),
    )


class StationStats(Base):
    __tablename__ = 'station_stat'
    station_id=Column(String)
    year=Column('year', Integer)
    max_mean_c=Column('max_mean_c', Numeric)
    min_mean_c=Column('min_mean_c', Numeric)
    precip_cm_total=Column('precip_cm_total', Numeric)
    extend_existing=True
    
    __table_args__ = (
        PrimaryKeyConstraint('station_id', 'year'),
    )

    