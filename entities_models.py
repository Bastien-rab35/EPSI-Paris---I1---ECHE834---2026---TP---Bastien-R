from dataclasses import dataclass, field
from sqlalchemy import MetaData, Table, Column, Integer, String, JSON
from sqlalchemy.orm import registry

mapper_registry = registry()

@dataclass
class Model:
    name: str
    pieces: list = field(default_factory=list)
    id: int = None

metadata_obj = MetaData()

models_table = Table(
    "models",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(100)),
    Column("pieces", JSON)
)

mapper_registry.map_imperatively(Model, models_table)
