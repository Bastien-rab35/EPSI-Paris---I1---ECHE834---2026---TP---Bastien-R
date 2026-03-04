import pytest
from service_models import app, engine, SERVICE_TOKEN
from entities_models import metadata_obj

@pytest.fixture()
def client():
    app.config.update({'TESTING': True})
    return app.test_client()

@pytest.fixture(scope='module')
def setup_db():
    metadata_obj.create_all(engine)
    yield
    metadata_obj.drop_all(engine)

def get_auth_headers():
    return {'Authorization': SERVICE_TOKEN}

def test_list_models_without_auth(client, setup_db):
    result = client.get('/models')
    assert result.status_code == 401

def test_create_model(client, setup_db):
    new_model = {
        'name': 'Voiture de course',
        'pieces': [1, 2, 3]
    }
    result = client.post('/models', json=new_model, headers=get_auth_headers())
    assert result.status_code == 201
    assert result.json['name'] == 'Voiture de course'

def test_add_piece_to_model(client, setup_db):
    model_data = {'name': 'Maison', 'pieces': []}
    create_result = client.post('/models', json=model_data, headers=get_auth_headers())
    model_id = create_result.json['id']
    
    result = client.post(f'/models/{model_id}/pieces', 
                        json={'piece_id': 5}, 
                        headers=get_auth_headers())
    assert result.status_code == 200
    assert 5 in result.json['pieces']

def test_get_used_pieces(client, setup_db):
    result = client.get('/used-pieces', headers=get_auth_headers())
    assert result.status_code == 200
    assert 'used_pieces' in result.json
