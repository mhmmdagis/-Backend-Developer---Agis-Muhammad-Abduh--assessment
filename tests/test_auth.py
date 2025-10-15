
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine
from app.seed import seed

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    seed()
    yield
    Base.metadata.drop_all(bind=engine)

def test_register_and_login():
    client = TestClient(app)
    res = client.post('/auth/register', json={'username':'dev1','email':'dev1@local','password':'pass123'})
    assert res.status_code == 200
    res2 = client.post('/auth/login', data={'email':'dev1@local','password':'pass123'})
    assert res2.status_code == 200
    data = res2.json()
    assert 'access_token' in data and 'refresh_token' in data

def test_refresh_token():
    client = TestClient(app)
    res = client.post('/auth/login', data={'email':'admin@local','password':'password123'})
    assert res.status_code == 200
    tokens = res.json()
    res2 = client.post('/auth/refresh', json={'refresh_token': tokens['refresh_token']})
    assert res2.status_code == 200
    assert 'access_token' in res2.json()
