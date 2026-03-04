from dataclasses import dataclass
from sqlalchemy import MetaData, Table, Column, Integer, String
from sqlalchemy.orm import registry

mapper_registry = registry()

@dataclass
class Piece:
    name: str
    color: str
    category: str
    id: int = None

metadata_obj = MetaData()

pieces_table = Table(
    "pieces",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(100)),
    Column("color", String(50)),
    Column("category", String(50))
)

mapper_registry.map_imperatively(Piece, pieces_table)
