import pytest
from service_pieces import app, engine
from entities_pieces import metadata_obj
from sqlalchemy.orm import Session

@pytest.fixture()
def client():
    app.config.update({'TESTING': True})
    return app.test_client()

@pytest.fixture(scope='module')
def setup_db():
    metadata_obj.create_all(engine)
    yield
    metadata_obj.drop_all(engine)

def test_create_piece(client, setup_db):
    new_piece = {
        'name': 'Brique 2x4',
        'color': 'rouge',
        'category': 'brique'
    }
    result = client.post('/pieces', json=new_piece)
    assert result.status_code == 201
    assert result.json['name'] == 'Brique 2x4'

def test_list_pieces(client, setup_db):
    result = client.get('/pieces')
    assert result.status_code == 200
    assert 'pieces' in result.json

def test_available_pieces(client, setup_db):
    result = client.get('/pieces/available')
    assert result.status_code == 200
    assert 'available_pieces' in result.json

def test_get_nonexistent_piece(client, setup_db):
    result = client.get('/pieces/99999')
    assert result.status_code == 404
