def test_health(client):
    r = client.get("/")
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["mock"] is True  # ensures MOCK_MODE in tests

def test_analyze_min_content_rejected(client):
    r = client.post("/analyze/", json={"content": "too short"})
    assert r.status_code == 422  # pydantic length rule

def test_analyze_ok(client):
    payload = {"url": "https://example.com", "title": "Example", "content": "This is a credible report with named sources and data points."}
    r = client.post("/analyze/", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert set(data.keys()) == {"analysis_id", "label", "score", "tips", "model_name", "created_at"}
    assert data["label"] in {"credible", "unknown", "misleading"}
    assert 0 <= data["score"] <= 100
    assert isinstance(data["tips"], list) and len(data["tips"]) >= 1
