def _make_analysis(client) -> str:
    r = client.post("/analyze/", json={"content": "Miracle cure shocking results"})
    return r.json()["analysis_id"]

def test_share_telegram_deeplink(client):
    analysis_id = _make_analysis(client)
    r = client.post("/share/", json={"analysis_id": analysis_id, "channel": "telegram"})
    assert r.status_code == 200
    out = r.json()
    assert "t.me" in out["deep_link_url"]
    assert out["token"]

def test_share_resolve_via_bot(client):
    analysis_id = _make_analysis(client)
    r = client.post("/share/", json={"analysis_id": analysis_id, "channel": "telegram"})
    token = r.json()["token"]

    # Bot resolves token to full analysis
    r2 = client.get(f"/bot/resolve/{token}")
    assert r2.status_code == 200
    payload = r2.json()
    assert payload["analysis_id"] and payload["label"] and 0 <= payload["score"] <= 100
