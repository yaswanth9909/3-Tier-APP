from fastapi.testclient import TestClient
from app import app  # because app.py is at repo root

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_home():
    r = client.get("/")
    assert r.status_code == 200
    body = r.json()
    assert "message" in body
    assert isinstance(body["message"], str)
