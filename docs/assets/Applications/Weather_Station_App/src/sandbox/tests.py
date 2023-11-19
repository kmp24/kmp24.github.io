import pytest
from app import app

# Add more tests!
def test_get_station_stats(client):
    response = client.get('/api/weather/stats?station_id=USC00339312&date=2012-07-01')
    assert response.get_json() == {
        'max_mean_c': '14.1060273973',
        'min_mean_c': '3.9550684932',
        'precip_cm_total': '100.6700000000',
        'station_id': 'USC00339312',
        'year': '1985'
    }

import 

def test_get_station_date(client):
    response = client.get('/api/weather?station_id=USC00339312&date=2012-07-01')
    assert response.get_json() == {
        'date': '2012-07-01',
        'max_temp_tenths_c': 317,
        'min_temp_tenths_c': 183,
        'precip_tenths_mm': 5,
        'station_id': 'USC00339312'
    }
