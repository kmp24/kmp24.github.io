from flask import Flask, jsonify, request
from data_model import WeatherData, StationStats
from constants import DATABASE_URI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

app = Flask(__name__)

def open_session(DATABASE_URI):
    # connect to db using session maker
    engine = create_engine(DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

@app.route('/api/weather', methods=['GET'])
def get_station():
    station_id = request.args.get('station_id')
    date_str = request.args.get('date')
    date = datetime.strptime(date_str, '%Y-%m-%d') if date_str else None

    session = open_session(DATABASE_URI)

    try:
        query = session.query(WeatherData).filter_by(station_id=station_id)

        if date:
            query = query.filter(WeatherData.date == date)

        weather_data = query.first()

        if weather_data:
            station_data = {
                'station_id': weather_data.station_id,
                'date': str(weather_data.date),
                'max_temp_tenths_c': weather_data.max_temp_tenths_c,
                'min_temp_tenths_c': weather_data.min_temp_tenths_c,
                'precip_tenths_mm': weather_data.precip_tenths_mm,
            }
            return jsonify(station_data)
        else:
            return jsonify({'message': 'No data found for station or date'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/weather/stats', methods=['GET'])
def get_station_totals():
    station_id = request.args.get('station_id')
    date_str = request.args.get('year')
    date = datetime.strptime(date_str, '%Y') if date_str else None

    session = open_session(DATABASE_URI)

    try:
        query = session.query(StationStats).filter_by(station_id=station_id)

        if date:
            query = query.filter(StationStats.year == year)

        weather_data = query.first()

        if weather_data:
            station_data = {
                'station_id': weather_data.station_id,
                'year': str(weather_data.year),
                'max_mean_c': weather_data.max_mean_c,
                'min_mean_c': weather_data.min_mean_c,
                'precip_cm_total': weather_data.precip_cm_total,
            }
            return jsonify(station_data)
        else:
            return jsonify({'message': 'No data found for station or date'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)