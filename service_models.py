from flask import Flask, request, jsonify
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from entities_models import metadata_obj, Model

app = Flask(__name__)
app.secret_key = b'lego_models_key'

engine = create_engine("sqlite:///models.db", echo=True)
metadata_obj.create_all(engine)

SERVICE_TOKEN = "Bearer lego_service_token_2026"

def check_auth():
    auth_header = request.headers.get('Authorization')
    return auth_header == SERVICE_TOKEN

@app.get('/models')
def list_models():
    if not check_auth():
        return {}, 401
    
    session_db = Session(engine)
    models = list(session_db.scalars(select(Model)))
    return {
        'models': [{'id': m.id, 'name': m.name, 'pieces': m.pieces} for m in models]
    }

@app.post('/models')
def create_model():
    if not check_auth():
        return {}, 401
    
    if 'name' not in request.json:
        return {}, 400
    
    model = Model(
        name=request.json['name'],
        pieces=request.json.get('pieces', [])
    )
    
    session_db = Session(engine)
    session_db.add(model)
    session_db.commit()
    result = jsonify({'id': model.id, 'name': model.name, 'pieces': model.pieces})
    return result, 201

@app.post('/models/<int:model_id>/pieces')
def add_piece_to_model(model_id):
    if not check_auth():
        return {}, 401
    
    if 'piece_id' not in request.json:
        return {}, 400
    session_db = Session(engine)
    model = session_db.get(Model, model_id)
    if not model:
        return {}, 404
    
    if model.pieces is None:
        model.pieces = []
    
    if request.json['piece_id'] not in model.pieces:
        model.pieces = model.pieces + [request.json['piece_id']]
        session_db.commit()
    
    
        return jsonify({'id': model.id, 'name': model.name, 'pieces': model.pieces})

@app.delete('/models/<int:model_id>/pieces/<int:piece_id>')
def remove_piece_from_model(model_id, piece_id):
    if not check_auth():
        return {}, 401
    session_db = Session(engine)
    model = session_db.get(Model, model_id)
    if not model:
        return {}, 404
    
    if model.pieces and piece_id in model.pieces:
        model.pieces = [p for p in model.pieces if p != piece_id]
        session_db.commit()
    
    return {'id': model.id, 'name': model.name, 'pieces': model.pieces}

@app.get('/used-pieces')
def get_used_pieces():
    if not check_auth():
        return {}, 401
    
    session_db = Session(engine)
    models = list(session_db.scalars(select(Model)))
    used_pieces = []
    for model in models:
        if model.pieces:
            used_pieces.extend(model.pieces)
    
    return {'used_pieces': list(set(used_pieces))}
