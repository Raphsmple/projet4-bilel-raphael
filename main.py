from enum import Enum

from fastapi import FastAPI, HTTPException
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
# MODELES DE REPONSE
# =========================

class ActorResponse(BaseModel):
    id: int
    name: str
    nationality: str


class TicketResponse(BaseModel):
    id: int
    session_id: int
    seat_number: int


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
# ROUTE PRINCIPALE
# =========================

@app.get("/")
def home():
    return {
        "message": "Cinema API opérationnelle"
    }


# =========================
# CRUD MOVIES
# =========================

@app.get("/movies")
def get_movies():
    return movies


@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    for movie in movies:
        if movie.id == movie_id:
            return movie

    raise HTTPException(
        status_code=404,
        detail="Film introuvable"
    )


@app.post("/movies")
def create_movie(movie: Movie):
    movies.append(movie)
    return movie


@app.patch("/movies/{movie_id}")
def update_movie(movie_id: int, updated_movie: Movie):
    for index, movie in enumerate(movies):
        if movie.id == movie_id:
            movies[index] = updated_movie
            return updated_movie

    raise HTTPException(
        status_code=404,
        detail="Film introuvable"
    )


@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    for index, movie in enumerate(movies):
        if movie.id == movie_id:
            deleted_movie = movies.pop(index)
            return deleted_movie

    raise HTTPException(
        status_code=404,
        detail="Film introuvable"
    )


# =========================
# CRUD ACTORS
# =========================

@app.get("/actors", response_model=list[ActorResponse])
def get_actors():
    return actors


@app.get("/actors/{actor_id}", response_model=ActorResponse)
def get_actor(actor_id: int):
    for actor in actors:
        if actor.id == actor_id:
            return actor

    raise HTTPException(
        status_code=404,
        detail="Acteur introuvable"
    )


@app.post("/actors")
def create_actor(actor: Actor):
    actors.append(actor)
    return actor


@app.patch("/actors/{actor_id}")
def update_actor(actor_id: int, updated_actor: Actor):
    for index, actor in enumerate(actors):
        if actor.id == actor_id:
            actors[index] = updated_actor
            return updated_actor

    raise HTTPException(
        status_code=404,
        detail="Acteur introuvable"
    )


@app.delete("/actors/{actor_id}")
def delete_actor(actor_id: int):
    for index, actor in enumerate(actors):
        if actor.id == actor_id:
            deleted_actor = actors.pop(index)
            return deleted_actor

    raise HTTPException(
        status_code=404,
        detail="Acteur introuvable"
    )


# =========================
# CRUD ROOMS
# =========================

@app.get("/rooms")
def get_rooms():
    return rooms


@app.get("/rooms/{room_id}")
def get_room(room_id: int):
    for room in rooms:
        if room.id == room_id:
            return room

    raise HTTPException(
        status_code=404,
        detail="Salle introuvable"
    )


@app.post("/rooms")
def create_room(room: Room):
    rooms.append(room)
    return room


@app.patch("/rooms/{room_id}")
def update_room(room_id: int, updated_room: Room):
    for index, room in enumerate(rooms):
        if room.id == room_id:
            rooms[index] = updated_room
            return updated_room

    raise HTTPException(
        status_code=404,
        detail="Salle introuvable"
    )


@app.delete("/rooms/{room_id}")
def delete_room(room_id: int):
    for index, room in enumerate(rooms):
        if room.id == room_id:
            deleted_room = rooms.pop(index)
            return deleted_room

    raise HTTPException(
        status_code=404,
        detail="Salle introuvable"
    )


# =========================
# CRUD SESSIONS
# =========================

@app.get("/sessions")
def get_sessions():
    return sessions


@app.get("/sessions/{session_id}")
def get_session(session_id: int):
    for session in sessions:
        if session.id == session_id:
            return session

    raise HTTPException(
        status_code=404,
        detail="Séance introuvable"
    )


@app.post("/sessions")
def create_session(session: Session):
    movie_exists = any(
        movie.id == session.movie_id
        for movie in movies
    )

    room_exists = any(
        room.id == session.room_id
        for room in rooms
    )

    if not movie_exists:
        raise HTTPException(
            status_code=404,
            detail="Le film associé à cette séance n'existe pas"
        )

    if not room_exists:
        raise HTTPException(
            status_code=404,
            detail="La salle associée à cette séance n'existe pas"
        )

    sessions.append(session)
    return session


@app.patch("/sessions/{session_id}")
def update_session(session_id: int, updated_session: Session):
    for index, session in enumerate(sessions):
        if session.id == session_id:
            sessions[index] = updated_session
            return updated_session

    raise HTTPException(
        status_code=404,
        detail="Séance introuvable"
    )


@app.delete("/sessions/{session_id}")
def delete_session(session_id: int):
    for index, session in enumerate(sessions):
        if session.id == session_id:
            deleted_session = sessions.pop(index)
            return deleted_session

    raise HTTPException(
        status_code=404,
        detail="Séance introuvable"
    )


# =========================
# CRUD TICKETS
# =========================

@app.get("/tickets", response_model=list[TicketResponse])
def get_tickets():
    return tickets


@app.get("/tickets/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: int):
    for ticket in tickets:
        if ticket.id == ticket_id:
            return ticket

    raise HTTPException(
        status_code=404,
        detail="Billet introuvable"
    )


@app.post("/tickets")
def create_ticket(ticket: Ticket):
    session_exists = any(
        session.id == ticket.session_id
        for session in sessions
    )

    if not session_exists:
        raise HTTPException(
            status_code=404,
            detail="La séance associée à ce billet n'existe pas"
        )

    tickets.append(ticket)
    return ticket


@app.patch("/tickets/{ticket_id}")
def update_ticket(ticket_id: int, updated_ticket: Ticket):
    for index, ticket in enumerate(tickets):
        if ticket.id == ticket_id:
            tickets[index] = updated_ticket
            return updated_ticket

    raise HTTPException(
        status_code=404,
        detail="Billet introuvable"
    )


@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: int):
    for index, ticket in enumerate(tickets):
        if ticket.id == ticket_id:
            deleted_ticket = tickets.pop(index)
            return deleted_ticket

    raise HTTPException(
        status_code=404,
        detail="Billet introuvable"
    )


# =========================
# RECHERCHE, FILTRES, TRI ET PAGINATION
# =========================

@app.get("/search/movies")
def search_movies(
    title: str | None = None,
    genre: MovieGenre | None = None,
    page: int = 1,
    limit: int = 10,
    sort_by: str = "title"
):
    result = movies

    if title is not None:
        result = [
            movie
            for movie in result
            if title.lower() in movie.title.lower()
        ]

    if genre is not None:
        result = [
            movie
            for movie in result
            if movie.genre == genre
        ]

    if sort_by == "title":
        result = sorted(
            result,
            key=lambda movie: movie.title
        )

    elif sort_by == "duration":
        result = sorted(
            result,
            key=lambda movie: movie.duration
        )

    start = (page - 1) * limit
    end = start + limit

    return {
        "page": page,
        "limit": limit,
        "total": len(result),
        "movies": result[start:end]
    }


# =========================
# STATISTIQUES
# =========================

@app.get("/stats")
def get_stats():
    total_movies = len(movies)
    total_actors = len(actors)
    total_rooms = len(rooms)
    total_sessions = len(sessions)
    total_tickets = len(tickets)

    total_revenue = sum(
        ticket.price
        for ticket in tickets
    )

    return {
        "total_movies": total_movies,
        "total_actors": total_actors,
        "total_rooms": total_rooms,
        "total_sessions": total_sessions,
        "total_tickets": total_tickets,
        "total_revenue": total_revenue
    }