"""
Filename: test_location_filtering.py
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
def test_map_view_filters_by_location(mock_load_table, client):
    # Mock data for stops
    stops_df = pd.DataFrame([
        {"stop_id": "1", "stop_name": "Nearby Stop", "stop_lat": 1.0, "stop_lon": 1.0},
        {"stop_id": "2", "stop_name": "Far Stop", "stop_lat": 50.0, "stop_lon": 50.0},
    ])
    # Mock routes
    routes_df = pd.DataFrame([
        {"route_id": "10", "route_long_name": "Route Near", "route_color": "FF0000"},
        {"route_id": "20", "route_long_name": "Route Far", "route_color": "00FF00"},
    ])
    stop_times_df = pd.DataFrame([{"trip_id": "t1", "stop_id": "1"}, {"trip_id": "t2", "stop_id": "2"}])
    trips_df = pd.DataFrame([{"trip_id": "t1", "route_id": "10", "shape_id": None},
                             {"trip_id": "t2", "route_id": "20", "shape_id": None}])
    shapes_df = pd.DataFrame([])

    mock_load_table.side_effect = [stops_df, routes_df, stop_times_df, trips_df, shapes_df]

    # Provide latitude/longitude near the first stop
    response = client.get("/map", query_string={"latitude": "1.0", "longitude": "1.0"})
    html = response.data.decode()

    # Should include nearby stop/route
    assert "Nearby Stop" in html
    assert "Route Near" in html

    # Should NOT include far stop/route
    assert "Far Stop" not in html
    assert "Route Far" not in html
