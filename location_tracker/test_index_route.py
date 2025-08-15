# test_index_route.py
import app_v2

def test_index_renders_ok():
    client = app_v2.app.test_client()
    resp = client.get("/")

    # Page should render successfully
    assert resp.status_code == 200
    # Should be HTML
    assert "text/html" in resp.content_type

    # Check for a stable piece of markup/text that always appears on the home page
    html = resp.get_data(as_text=True)
    assert "Transit Tracker" in html  # title/text on the page
