from fastapi import status


def test_get_weather(client, populate_db):
    """Test for weather api endpoint"""
    response = client.get("/weather?offset=0&limit=1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "date": "1985-01-01",
            "id": 1,
            "maximum_temp": -22.0,
            "minimum_temp": -128.0,
            "precipitation": 94.0,
            "station_id": "USC00110187",
        }
    ]


def test_get_weather_filter_by_date(client, populate_db):
    """Test for weather api endpoint filtered by date"""
    response = client.get(
        "/weather?date=19850101& \
        offset=0&limit=1"
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "date": "1985-01-01",
            "id": 1,
            "maximum_temp": -22.0,
            "minimum_temp": -128.0,
            "precipitation": 94.0,
            "station_id": "USC00110187",
        }
    ]


def test_get_weather_filter_by_station(client, populate_db):
    """Test for weather api endpoint filtered by station_id"""

    response = client.get(
        "/weather?station_id=USC00110187& \
        offset=0&limit=1"
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "date": "1985-01-01",
            "id": 1,
            "maximum_temp": -22.0,
            "minimum_temp": -128.0,
            "precipitation": 94.0,
            "station_id": "USC00110187",
        }
    ]


def test_get_weather_filter_by_station_and_date(client, populate_db):
    """Test for weather api endpoint filtered by date and station_id"""

    response = client.get(
        "/weather?station_id=USC00110187& \
        date=19850101&offset=0&limit=1"
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "date": "1985-01-01",
            "id": 1,
            "maximum_temp": -22.0,
            "minimum_temp": -128.0,
            "precipitation": 94.0,
            "station_id": "USC00110187",
        }
    ]


def test_get_weather_invalid_date(client):
    """Test for weather api endpoint with invalid date"""
    response = client.get("/weather?date=111offset=0&limit=1")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_weather_invalid_station(client):
    """Test for weather api endpoint with invalid station id"""
    response = client.get("/weather?station_id=111offset=0&limit=1")
    assert response.status_code == status.HTTP_404_NOT_FOUND
