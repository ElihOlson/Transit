# test_forecast_api.py
import app_v2

def test_forecast_api_success(monkeypatch):
    # Stub out heavy functions so no DB/time dependence
    def fake_forecast(stop_id, route_name, return_only=False):
        assert stop_id == 123 and route_name == "ORBT"
        # match function signature: return (next_time, capacity_status)
        return ("2025-08-15 07:45:00 AM", "<span style='color:red;'>At Max Capacity</span>")

    def fake_capacity(route_name):
        return "OK"  # simple, predictable output for test

    monkeypatch.setattr(app_v2, "forecast", fake_forecast)
    monkeypatch.setattr(app_v2, "get_bus_capacity_status", fake_capacity)

    client = app_v2.app.test_client()
    resp = client.get("/forecast_api?stop_id=123&route_name=ORBT")

    assert resp.status_code == 200
    data = resp.get_json()
    assert data["stop_id"] == 123
    assert data["route_name"] == "ORBT"
    assert data["next_arrival"] == "2025-08-15 07:45:00 AM"
    assert data["bus_capacity"] == "OK"

def test_forecast_api_missing_params():
    client = app_v2.app.test_client()
    resp = client.get("/forecast_api")  # no params
    assert resp.status_code == 400

def test_forecast_api_handles_error(monkeypatch):
    def boom(*args, **kwargs):
        raise ValueError("boom")
    monkeypatch.setattr(app_v2, "forecast", boom)

    client = app_v2.app.test_client()
    resp = client.get("/forecast_api?stop_id=1&route_name=Any")
    assert resp.status_code == 500
    assert "error" in resp.get_json()
