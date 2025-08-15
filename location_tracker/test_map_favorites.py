"""
Filename: test_map_favorites.py
Last Written: Derek (8/15/25)
"""

import pytest
import pandas as pd
from unittest.mock import patch
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@patch("app.load_table")
def test_map_view_shows_all_when_no_favorites(mock_load_table, client):
    # Mock data
    stops_df = pd.DataFrame([
        {"stop_id": "1", "stop_name": "Stop A", "stop_lat": 1.0, "stop_lon": 1.0},
        {"stop_id": "2", "stop_name": "Stop B", "stop_lat": 2.0, "stop_lon": 2.0},
    ])
    routes_df = pd.DataFrame([
        {"route_id": "10", "route_long_name": "Route X", "route_color": "FF0000"},
        {"route_id": "20", "route_long_name": "Route Y", "route_color": "00FF00"},
    ])
    stop_times_df = pd.DataFrame([{"trip_id": "t1", "stop_id": "1"}, {"trip_id": "t2", "stop_id": "2"}])
    trips_df = pd.DataFrame([{"trip_id": "t1", "route_id": "10", "shape_id": None},
                             {"trip_id": "t2", "route_id": "20", "shape_id": None}])
    shapes_df = pd.DataFrame([])

    mock_load_table.side_effect = [stops_df, routes_df, stop_times_df, trips_df, shapes_df]

    response = client.get("/map")  # no favorites params
    html = response.data.decode()

    # All stops and routes should appear
    assert "Stop A" in html
    assert "Stop B" in html
    assert "Route X" in html
    assert "Route Y" in html
