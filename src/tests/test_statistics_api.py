from fastapi import status


def test_get_stats(client, populate_db):
    """Test for Stats api endpoint"""
    response = client.get("/weather/stats?offset=0&limit=1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "id": 1,
            "station_id": "USC00110187",
            "year": 1985,
            "avg_max_temp": -31.2,
            "avg_min_temp": -122.9,
            "total_precipitation": 109.0,
        }
    ]


def test_get_stats_filter_by_year(client, populate_db):
    """Test for stats api endpoint filtered by date"""
    response = client.get(
        "/weather/stats?year=1985& \
        offset=0&limit=1"
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "id": 1,
            "station_id": "USC00110187",
            "year": 1985,
            "avg_max_temp": -31.2,
            "avg_min_temp": -122.9,
            "total_precipitation": 109.0,
        }
    ]


def test_get_stats_filter_by_station(client, populate_db):
    """Test for Stats api endpoint filtered by station_id"""

    response = client.get(
        "/weather/stats?station_id=USC00110187& \
        offset=0&limit=1"
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "id": 1,
            "station_id": "USC00110187",
            "year": 1985,
            "avg_max_temp": -31.2,
            "avg_min_temp": -122.9,
            "total_precipitation": 109.0,
        }
    ]


def test_get_stats_filter_by_station_and_year(client, populate_db):
    """Test for stats api endpoint filtered by date and station_id"""

    response = client.get(
        "/weather/stats?station_id=USC00110187& \
        year=1985&offset=0&limit=1"
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "id": 1,
            "station_id": "USC00110187",
            "year": 1985,
            "avg_max_temp": -31.2,
            "avg_min_temp": -122.9,
            "total_precipitation": 109.0,
        }
    ]


def test_get_stats_invalid_year(client):
    """Test for stats api endpoint with invalid date"""
    response = client.get("/weather/stats?offset=0&limit=2&year=20")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_stats_invalid_station(client):
    """Test for stats api endpoint with invalid station id"""
    response = client.get("/weather/stats?station_id=111offset=0&limit=1")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_stats_invalid_offset(client):
    """Test for stats api endpoint with invalid offset"""
    response = client.get("/weather/stats?offset=10&limit=1")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["message"] == "Couldn't fetch data: No data found at given offset"
