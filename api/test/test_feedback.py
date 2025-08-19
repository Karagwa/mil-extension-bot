def _make_analysis(client) -> str:
    r = client.post("/analyze/", json={"content": "Opinion blog about tech"})
    return r.json()["analysis_id"]

def test_feedback_records_ok(client):
    analysis_id = _make_analysis(client)
    r = client.post("/feedback/", json={"analysis_id": analysis_id, "helpful": True, "source": "extension"})
    assert r.status_code == 200
    assert r.json()["ok"] is True
