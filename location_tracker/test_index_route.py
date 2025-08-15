# test_index_route.py
import app_v2

def test_index_renders_ok(monkeypatch):
    # Make capacity text predictable
    monkeypatch.setattr(app_v2, "get_bus_capacity_status", lambda route: "OK-STATUS")

    client = app_v2.app.test_client()
    resp = client.get("/")

    # Page should render successfully
    assert resp.status_code == 200
    # Should be HTML
    assert "text/html" in resp.content_type

    # If the template renders the variable, we should see it in the HTML
    html = resp.get_data(as_text=True)
    assert "OK-STATUS" in html
