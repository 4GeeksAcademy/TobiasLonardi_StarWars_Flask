from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, DateTime, func, Text, Table, Column,Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
import enum

db = SQLAlchemy()

class CharacterSide(enum.Enum):
    LIGHTSIDE = "lightSide"
    DARKSIDE = "darkSide"
    NEUTRAL = "neutral"

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
    favorites_planets: Mapped[List["FavoritePlanet"]] = relationship("FavoritePlanet",back_populates="owner")
    favorites_character: Mapped[List["FavoriteCharacter"]] = relationship("FavoriteCharacter", back_populates="owner")

    def serialize(self):
        return{
            "id":self.id,
            "name": self.name,
            "username": self.username,
            "favorites_planets": self.favorites_planets,
            "favorites_character": self.favorites_character
        }

class Planet(db.Model):
    __tablename__ = "planet"
    id:Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    description: Mapped[str] = mapped_column(String(160))
    population: Mapped[int] = mapped_column(nullable=False)
    favorites_planets: Mapped[List["FavoritePlanet"]] = relationship("FavoritePlanet",back_populates="planet")

    def serialize(self):
        return{
            "id":self.id,
            "name": self.name,
            "description": self.description,
            "population":self.population,
        }


class Character(db.Model):
    __tablename__ = "character"
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(100),nullable=False)
    gender:Mapped[enum] = mapped_column(Enum(CharactersGenders))
    side:Mapped[enum] = mapped_column(Enum(CharacterSide))
    favorites_characters: Mapped[List["FavoriteCharacter"]] = relationship("FavoriteCharacter", back_populates="character")

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "gender":self.gender.value,
            "side":self.side.value,

        }

class FavoritePlanet(db.Model):
    __tablename__ = "favorites_planets"
    id:Mapped[int] = mapped_column(primary_key=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    owner: Mapped["User"] = relationship("User",back_populates="favorites_planets")
    planet: Mapped["Planet"] = relationship("Planet",back_populates="favorites_planets")

    def serialize(self):
        return{
            "id":self.id,
            "planet_id": self.planet_id,
            "user_id": self.user_id

        }


class FavoriteCharacter(db.Model):
    __tablename__ = "favorites_characters"
    id:Mapped[int] = mapped_column(primary_key=True)
    character_id:Mapped[int] = mapped_column(ForeignKey("character.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    owner: Mapped["User"] = relationship("User",back_populates="favorites_character")
    character: Mapped["Character"] = relationship("Character", back_populates="favorites_characters")
    def serialize(self):
        return{
            "id":self.id,
            "character_id": self.character_id,
            "user_id": self.user_id

        }

    







