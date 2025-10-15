
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine
from app.seed import seed

def setup_module(module):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    seed()

def test_create_task_and_list():
    client = TestClient(app)
    res = client.post('/auth/login', data={'email':'admin@local','password':'password123'})
    tokens = res.json()
    headers = {'Authorization': f"Bearer {tokens['access_token']}"}
    res2 = client.post('/tasks/', json={'title':'T1','description':'desc'}, headers=headers)
    assert res2.status_code == 200
    task = res2.json()
    assert task['title'] == 'T1'
    res3 = client.get('/tasks/')
    assert res3.status_code == 200
    assert isinstance(res3.json(), list)
