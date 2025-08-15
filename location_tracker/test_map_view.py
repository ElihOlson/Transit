"""
Filename: test_map_view.py
Last Written: Derek (8/15/25)
"""

import pytest
from unittest.mock import patch
import pandas as pd
from app import app 

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@patch("app.load_table")
def test_map_view_shows_only_favorites(mock_load_table, client):
    # Mock data for stops
    stops_df = pd.DataFrame([
        {"stop_id": "1", "stop_name": "Favorite Stop", "stop_lat": 1.0, "stop_lon": 1.0},
        {"stop_id": "2", "stop_name": "Other Stop", "stop_lat": 2.0, "stop_lon": 2.0},
    ])

    # Mock data for routes
    routes_df = pd.DataFrame([
        {"route_id": "10", "route_long_name": "Favorite Route", "route_color": "FF0000"},
        {"route_id": "20", "route_long_name": "Other Route", "route_color": "00FF00"},
    ])

    # Mock data for stop_times
    stop_times_df = pd.DataFrame([
        {"trip_id": "t1", "stop_id": "1"},
        {"trip_id": "t2", "stop_id": "2"}
    ])

    # Mock data for trips
    trips_df = pd.DataFrame([
        {"trip_id": "t1", "route_id": "10", "shape_id": None},
        {"trip_id": "t2", "route_id": "20", "shape_id": None}
    ])

    # Mock shapes table
    shapes_df = pd.DataFrame([])

    # Side effects in the exact order map_view() calls load_table()
    mock_load_table.side_effect = [
        stops_df,      # stops
        routes_df,     # routes
        stop_times_df, # stop_times
        trips_df,      # trips
        shapes_df      # shapes
    ]

    # Perform GET with favorites filter
    response = client.get("/map", query_string={
        "latitude": "0",
        "longitude": "0",
        "show_favorites_only": "1",
        "favorite_routes": "Favorite Route",
        "favorite_stops": "1"
    })

    html = response.data.decode()

    # Should include favorite stop marker
    assert "Favorite Stop" in html

    # Should NOT include non-favorite stop marker
    assert "Other Stop" not in html

