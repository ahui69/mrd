import os, io
from fastapi.testclient import TestClient
import monolit as M

AUTH = os.getenv('AUTH_TOKEN','changeme')
client = TestClient(M.app)


def auth():
    return {"Authorization": f"Bearer {AUTH}"}


def test_health():
    r = client.get('/api/health')
    assert r.status_code == 200
    assert r.json().get('ok') is True


def test_assistant_chat_minimal():
    p = {"user":"user","messages":[{"role":"user","content":"Cześć!"}]}
    r = client.post('/api/assistant/chat', json=p, headers=auth())
    assert r.status_code == 200
    j = r.json()
    assert 'ok' in j and 'answer' in j


def test_writer_routes_exist():
    # creative
    body = {"topic":"test","min_words":30,"max_words":60}
    r = client.post('/api/write/creative', json=body, headers=auth())
    assert r.status_code in (200, 500, 401)


def test_semantic_routes_exist():
    r = client.post('/api/semantic/analyze', json={"text":"Ala ma kota"}, headers=auth())
    assert r.status_code in (200, 500, 401)


def test_files_upload_roundtrip(tmp_path):
    data = io.BytesIO(b"hello")
    files = {"files": ("hello.txt", data, "text/plain")}
    r = client.post('/api/files/upload', files=files, headers=auth())
    assert r.status_code == 200
    j = r.json()
    assert j.get('ok') is True and j.get('files')


def test_stt_requires_keys():
    data = io.BytesIO(b"RIFF....fake...")
    files = {"audio": ("a.wav", data, "audio/wav")}
    r = client.post('/api/stt/transcribe', files=files, headers=auth())
    assert r.status_code in (200, 400)


def test_ltm_endpoints_exist():
    r = client.post('/api/ltm/add', json={"text":"fakt"}, headers=auth())
    assert r.status_code in (200, 500)
    r = client.get('/api/ltm/search', params={"q":"fakt"}, headers=auth())
    assert r.status_code in (200, 500)
