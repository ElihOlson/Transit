import app_v2

def set_now(monkeypatch, hour, minute):
    """Monkeypatch app_v2.datetime.now() to a fixed time today."""
    real_dt = app_v2.datetime

    class FixedDateTime(real_dt):
        @classmethod
        def now(cls, tz=None):
            return real_dt(2025, 8, 15, hour, minute)

    monkeypatch.setattr(app_v2, "datetime", FixedDateTime)

def test_popular_route_is_max_capacity_even_offpeak(monkeypatch):
    set_now(monkeypatch, 11, 0)
    html = app_v2.get_bus_capacity_status("ORBT")
    assert "Max Capacity" in html

def test_nonpopular_route_open_seats_offpeak(monkeypatch):
    set_now(monkeypatch, 11, 0)
    html = app_v2.get_bus_capacity_status("Some Local Route")
    assert "Open Seats" in html

def test_nonpopular_route_full_standing_only_in_peak(monkeypatch):
    set_now(monkeypatch, 16, 30)
    html = app_v2.get_bus_capacity_status("Some Local Route")
    assert "Full Standing Only" in html

def test_average_bus_status_peak_vs_offpeak(monkeypatch):
    set_now(monkeypatch, 7, 0)
    peak_html = app_v2.get_average_bus_status()
    assert "Limited Space" in peak_html

    set_now(monkeypatch, 11, 0)
    offpeak_html = app_v2.get_average_bus_status()
    assert "Available spaces" in offpeak_html

def test_get_upcoming_capacity_true_false():
    assert "Full Standing Only" in app_v2.get_upcoming_capacity(True)
    assert app_v2.get_upcoming_capacity(False) is None

