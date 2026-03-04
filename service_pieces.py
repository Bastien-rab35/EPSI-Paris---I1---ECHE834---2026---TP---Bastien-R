from flask import Flask, request, jsonify
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from entities_pieces import Piece, metadata_obj
import requests

app = Flask(__name__)
app.secret_key = b'lego_secret_key'

engine = create_engine("sqlite:///pieces.db", echo=True)
metadata_obj.create_all(engine)

SERVICE_MODELS_URL = "http://localhost:5001"
SERVICE_TOKEN = "Bearer lego_service_token_2026"

def get_used_pieces():
    try:
        response = requests.get(
            f"{SERVICE_MODELS_URL}/used-pieces",
            headers={"Authorization": SERVICE_TOKEN}
        )
        if response.status_code == 200:
            return response.json().get('used_pieces', [])
    except:
        pass
    return []

@app.get('/pieces')
def list_pieces():
    session_db = Session(engine)
    pieces = list(session_db.scalars(select(Piece)))
    return {
        'pieces': [{'id': p.id, 'name': p.name, 'color': p.color, 'category': p.category} for p in pieces]
    }

@app.post('/pieces')
def create_piece():
    if not all(k in request.json for k in ['name', 'color', 'category']):
        return {}, 400
    
    piece = Piece(
        name=request.json['name'],
        color=request.json['color'],
        category=request.json['category']
    )
    
    session_db = Session(engine)
    session_db.add(piece)
    session_db.commit()
    result = jsonify({'id': piece.id, 'name': piece.name, 'color': piece.color, 'category': piece.category})
    return result, 201

@app.get('/pieces/available')
def list_available_pieces():
    used_pieces = get_used_pieces()
    
    session_db = Session(engine)
    all_pieces = list(session_db.scalars(select(Piece)))
    available = [
        {'id': p.id, 'name': p.name, 'color': p.color, 'category': p.category}
        for p in all_pieces if p.id not in used_pieces
    ]
    return {'available_pieces': available}

@app.get('/pieces/<int:piece_id>')
def get_piece(piece_id):
    session_db = Session(engine)
    piece = session_db.get(Piece, piece_id)
    if not piece:
        return {}, 404
    return {'id': piece.id, 'name': piece.name, 'color': piece.color, 'category': piece.category}
