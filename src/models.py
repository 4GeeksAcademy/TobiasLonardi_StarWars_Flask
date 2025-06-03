from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, DateTime, func, Text, Table, Column,Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

db = SQLAlchemy()

class CharactersGenders(enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class User(db.Model):
    __tablename__ = "user"
    id:Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    username: Mapped[str] = mapped_column(String(80), nullable=False)
    password: Mapped[str] = mapped_column(String(80), nullable=False)

class Planet(db.Model):
    __tablename__ = "planet"
    id:Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    description: Mapped[str] = mapped_column(String(160))
    population: Mapped[int] = mapped_column(nullable=False)

class Character(db.Model):
    __tablename__ = "character"
    id:Mapped[int] = mapped_column(primary_key=True)
    gender:Mapped[enum] = mapped_column(Enum(CharactersGenders))




