from app import BaseModel, db

venue_and_genre = db.Table(
    "venue_and_genre",
    db.Column("venue_id", db.Integer, db.ForeignKey("venue.id")),
    db.Column("genre_id", db.Integer, db.ForeignKey("genre.id")),
)


artist_and_genre = db.Table(
    "artist_and_genre",
    db.Column("artist_id", db.Integer, db.ForeignKey("artist.id")),
    db.Column("genre_id", db.Integer, db.ForeignKey("genre.id")),
)


class Venue(BaseModel):
    __tablename__ = "venue"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship("Show", backref="venue_shows")
    genres = db.relationship("Genre", secondary=venue_and_genre, backref="venue_genres")


class Artist(BaseModel):
    __tablename__ = "artist"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship("Show", backref="artist_shows")
    genres = db.relationship(
        "Genre", secondary=artist_and_genre, backref="artist_genres"
    )


class Show(BaseModel):
    __tablename__ = "show"

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey("venue.id"), nullable=False)
    venue_name = db.Column(db.String, nullable=False)
    venue_image_link = db.Column(db.String(500))
    artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"), nullable=False)
    artist_name = db.Column(db.String, nullable=False)
    artist_image_link = db.Column(db.String(500))
    start_time = db.Column(db.DateTime, nullable=False)


class Genre(BaseModel):
    __tablename__ = "genre"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True, nullable=False)
