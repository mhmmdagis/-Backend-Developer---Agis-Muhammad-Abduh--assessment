
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine
from app.seed import seed

def setup_module(module):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    seed()

def test_me_endpoint():
    client = TestClient(app)
    res = client.post('/auth/login', data={'email':'admin@local','password':'password123'})
    tokens = res.json()
    headers = {'Authorization': f"Bearer {tokens['access_token']}"}
    res2 = client.get('/users/me', headers=headers)
    assert res2.status_code == 200
    data = res2.json()
    assert data['email'] == 'admin@local'
