from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator, model_validator


app = FastAPI(title="Cinema API")


# =========================
# ENUMS
# =========================

class MovieGenre(str, Enum):
    ACTION = "action"
    COMEDY = "comedy"
    HORROR = "horror"
    SCIENCE_FICTION = "science-fiction"
    DRAMA = "drama"


class SessionStatus(str, Enum):
    AVAILABLE = "available"
    FULL = "full"
    CANCELLED = "cancelled"


# =========================
# MODELES
# =========================

class CastMember(BaseModel):
    actor_id: int
    role: str = Field(min_length=2, max_length=100)


class Movie(BaseModel):
    id: int
    title: str = Field(min_length=2, max_length=100)
    duration: int = Field(gt=0, le=300)
    genre: MovieGenre
    description: str | None = None
    cast: list[CastMember] = Field(default_factory=list)

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        if value.strip() == "":
            raise ValueError("Le titre ne peut pas être vide")
        return value.strip()

    @model_validator(mode="after")
    def validate_horror_duration(self):
        if self.genre == MovieGenre.HORROR and self.duration < 60:
            raise ValueError(
                "Un film d'horreur doit durer au moins 60 minutes"
            )
        return self


class Actor(BaseModel):
    id: int
    name: str = Field(min_length=2, max_length=100)
    age: int = Field(ge=0, le=120)
    nationality: str = Field(min_length=2, max_length=50)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if value.strip() == "":
            raise ValueError("Le nom ne peut pas être vide")
        return value.strip()


class Room(BaseModel):
    id: int
    name: str = Field(min_length=2, max_length=50)
    capacity: int = Field(gt=0, le=500)


class Session(BaseModel):
    id: int
    movie_id: int
    room_id: int
    start_hour: int = Field(ge=0, le=23)
    end_hour: int = Field(ge=0, le=23)
    status: SessionStatus = SessionStatus.AVAILABLE

    @model_validator(mode="after")
    def validate_hours(self):
        if self.end_hour <= self.start_hour:
            raise ValueError(
                "L'heure de fin doit être après l'heure de début"
            )
        return self


class Ticket(BaseModel):
    id: int
    session_id: int
    customer_name: str = Field(min_length=2, max_length=100)
    seat_number: int = Field(gt=0, le=500)
    price: float = Field(gt=0, le=100)


# =========================
# DONNEES DE DEPART
# =========================

movies = [
    Movie(
        id=1,
        title="Interstellar",
        duration=169,
        genre=MovieGenre.SCIENCE_FICTION,
        description="Un voyage spatial à travers les étoiles.",
        cast=[
            CastMember(actor_id=1, role="Cooper"),
            CastMember(actor_id=2, role="Brand"),
        ],
    ),
    Movie(
        id=2,
        title="Le Roi Lion",
        duration=88,
        genre=MovieGenre.DRAMA,
        description="L'histoire de Simba.",
        cast=[
            CastMember(actor_id=3, role="Simba"),
        ],
    ),
]

actors = [
    Actor(
        id=1,
        name="Matthew McConaughey",
        age=56,
        nationality="American",
    ),
    Actor(
        id=2,
        name="Anne Hathaway",
        age=43,
        nationality="American",
    ),
    Actor(
        id=3,
        name="Donald Glover",
        age=42,
        nationality="American",
    ),
]

rooms = [
    Room(
        id=1,
        name="Salle 1",
        capacity=200,
    ),
    Room(
        id=2,
        name="Salle 2",
        capacity=100,
    ),
]

sessions = [
    Session(
        id=1,
        movie_id=1,
        room_id=1,
        start_hour=18,
        end_hour=21,
        status=SessionStatus.AVAILABLE,
    ),
    Session(
        id=2,
        movie_id=2,
        room_id=2,
        start_hour=20,
        end_hour=22,
        status=SessionStatus.AVAILABLE,
    ),
]

tickets = [
    Ticket(
        id=1,
        session_id=1,
        customer_name="Raphael",
        seat_number=25,
        price=12.50,
    ),
    Ticket(
        id=2,
        session_id=2,
        customer_name="Bilel",
        seat_number=10,
        price=10.00,
    ),
]


# =========================
# ROUTE DE TEST
# =========================

@app.get("/")
def home():
    return {
        "message": "Cinema API opérationnelle"
    }