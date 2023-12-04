from janeiro.database import Entity, Database
from sqlalchemy import Column, Integer, String

db = Database("sqlite:///db.sqlite", "db_migrations")

class Account(Entity):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)

class Group(Entity):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)