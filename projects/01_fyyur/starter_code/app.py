# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import datetime
import logging
from logging import FileHandler, Formatter
from typing import Dict, List

import babel
import dateutil.parser
from dateutil import parser
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model
from sqlalchemy import func, inspect
from sqlalchemy.orm import exc

from forms import *

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object("config")
db = SQLAlchemy(app)
migrate = Migrate(app=app, db=db)

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#


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


class Venue(db.Model):
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


class Artist(db.Model):
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


class Show(db.Model):
    __tablename__ = "show"

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey("venue.id"), nullable=False)
    venue_name = db.Column(db.String, nullable=False)
    venue_image_link = db.Column(db.String(500))
    artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"), nullable=False)
    artist_name = db.Column(db.String, nullable=False)
    artist_image_link = db.Column(db.String(500))
    start_time = db.Column(db.DateTime, nullable=False)


class Genre(db.Model):
    __tablename__ = "genre"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True, nullable=False)


def model_to_dict(obj: Model) -> Dict:
    results = dict()
    for col in inspect(obj).mapper.column_attrs:
        value = getattr(obj, col.key)
        if isinstance(value, datetime):
            results[col.key] = value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            results[col.key] = value
    return results


def compose_show_attributes(shows: List[Model]) -> Dict:
    past_shows = list(filter(lambda show: show.start_time <= datetime.now(), shows))
    upcoming_shows = list(filter(lambda show: show.start_time > datetime.now(), shows))

    return {
        "past_shows": [model_to_dict(show) for show in past_shows],
        "upcoming_shows": [model_to_dict(show) for show in upcoming_shows],
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format="medium"):
    date = dateutil.parser.parse(value)
    if format == "full":
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == "medium":
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


def filter_dict_by_keys(input_dict: Dict, keep_keys: List):
    return {key: value for key, value in input_dict.items() if key in keep_keys}


app.jinja_env.filters["datetime"] = format_datetime

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route("/")
def index():
    return render_template("pages/home.html")


#  Venues
#  ----------------------------------------------------------------


@app.route("/venues")
def venues():
    groups = (
        Venue.query.with_entities(Venue.city, Venue.state, func.array_agg(Venue.id))
        .group_by(Venue.city, Venue.state)
        .all()
    )

    data = []
    for group in groups:
        venues = []
        for venue_id in group[2]:
            venue_data = Venue.query.filter_by(id=venue_id).one()
            venue_dict = model_to_dict(venue_data)
            venue_dict = filter_dict_by_keys(venue_dict, ["id", "name"])

            venue_shows = venue_data.shows
            shows_dict = compose_show_attributes(venue_shows)
            shows_dict = {"num_upcoming_shows": shows_dict["upcoming_shows_count"]}

            venue_dict.update(shows_dict)
            venues.append(venue_dict)
        data.append({"city": group[0], "state": group[1], "venues": venues})

    return render_template("pages/venues.html", areas=data)


@app.route("/venues/search", methods=["POST"])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    response = {
        "count": 1,
        "data": [{"id": 2, "name": "The Dueling Pianos Bar", "num_upcoming_shows": 0,}],
    }
    return render_template(
        "pages/search_venues.html",
        results=response,
        search_term=request.form.get("search_term", ""),
    )


@app.route("/venues/<int:venue_id>")
def show_venue(venue_id):
    venue_data = Venue.query.filter_by(id=venue_id).one()
    venue_dict = model_to_dict(venue_data)
    venue_shows = venue_data.shows

    shows_dict = compose_show_attributes(venue_shows)
    venue_dict.update(shows_dict)
    # TODO: fix GET /venues/None HTTP/1.0" 405
    return render_template("pages/show_venue.html", venue=venue_dict)


#  Create Venue
#  ----------------------------------------------------------------


@app.route("/venues/create", methods=["GET"])
def create_venue_form():
    form = VenueForm()
    return render_template("forms/new_venue.html", form=form)


@app.route("/venues/create", methods=["POST"])
def create_venue_submission():
    form_data = request.form.to_dict()
    venue_name = request.form["name"]
    genres = form_data.pop("genres")
    if isinstance(genres, str):
        genres = [genres]

    venue = Venue(**form_data)
    venue.genres = Genre.query.filter(Genre.name.in_(genres)).all()

    try:
        db.session.add(venue)
        db.session.commit()
        flash(f"Venue {venue_name} was successfully listed!")
    except:
        db.session.rollback()
        flash(f"An error occurred. Venue {venue_name} could not be listed.")

    return render_template("pages/home.html")


@app.route("/venues/<venue_id>", methods=["POST"])
def delete_venue(venue_id):
    try:
        venue = Venue.query.filter_by(id=venue_id).one()
        db.session.delete(venue)
        db.session.commit()
        flash(f"Venue id {venue_id} was successfully deleted!")
    except:
        db.session.rollback()
        flash(f"An error occurred. Venue id {venue_id} could not be deleted.")

    return render_template("pages/home.html")


#  Artists
#  ----------------------------------------------------------------
@app.route("/artists")
def artists():
    return render_template("pages/artists.html", artists=Artist.query.all())


@app.route("/artists/search", methods=["POST"])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    response = {
        "count": 1,
        "data": [{"id": 4, "name": "Guns N Petals", "num_upcoming_shows": 0,}],
    }
    return render_template(
        "pages/search_artists.html",
        results=response,
        search_term=request.form.get("search_term", ""),
    )


@app.route("/artists/<int:artist_id>")
def show_artist(artist_id):
    artist_data = Artist.query.filter_by(id=artist_id).one()
    artist_dict = model_to_dict(artist_data)
    artist_shows = artist_data.shows

    shows_dict = compose_show_attributes(artist_shows)
    artist_dict.update(shows_dict)

    return render_template("pages/show_artist.html", artist=artist_dict)


#  Update
#  ----------------------------------------------------------------
@app.route("/artists/<int:artist_id>/edit", methods=["GET"])
def edit_artist(artist_id):
    form = ArtistForm()
    artist_data = Artist.query.filter_by(id=artist_id).one()
    artist_dict = model_to_dict(artist_data)
    return render_template("forms/edit_artist.html", form=form, artist=artist_dict)


@app.route("/artists/<int:artist_id>/edit", methods=["POST"])
def edit_artist_submission(artist_id):
    form_data = request.form.to_dict()
    artist_name = request.form["name"]
    genres = form_data.pop("genres")
    if isinstance(genres, str):
        genres = [genres]

    artist = Artist.query.filter_by(id=artist_id).one()
    artist.genres = Genre.query.filter(Genre.name.in_(genres)).all()
    for key, value in form_data.items():
        setattr(artist, key, value)

    try:
        db.session.commit()
        flash(f"Artist {artist_name} was successfully updated!")
    except:
        db.session.rollback()
        flash(f"An error occurred. Artist {artist_name} could not be updated.")

    return redirect(url_for("show_artist", artist_id=artist_id))


@app.route("/venues/<int:venue_id>/edit", methods=["GET"])
def edit_venue(venue_id):
    form = VenueForm()
    venue_data = Venue.query.filter_by(id=venue_id).one()
    venue_dict = model_to_dict(venue_data)
    return render_template("forms/edit_venue.html", form=form, venue=venue_dict)


@app.route("/venues/<int:venue_id>/edit", methods=["POST"])
def edit_venue_submission(venue_id):
    form_data = request.form.to_dict()
    venue_name = request.form["name"]
    genres = form_data.pop("genres")
    if isinstance(genres, str):
        genres = [genres]

    venue = Venue.query.filter_by(id=venue_id).one()
    venue.genres = Genre.query.filter(Genre.name.in_(genres)).all()
    for key, value in form_data.items():
        setattr(venue, key, value)

    try:
        db.session.commit()
        flash(f"Artist {venue_name} was successfully updated!")
    except:
        db.session.rollback()
        flash(f"An error occurred. Artist {venue_name} could not be updated.")

    return redirect(url_for("show_venue", venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------


@app.route("/artists/create", methods=["GET"])
def create_artist_form():
    form = ArtistForm()
    return render_template("forms/new_artist.html", form=form)


@app.route("/artists/create", methods=["POST"])
def create_artist_submission():
    form_data = request.form.to_dict()
    artist_name = request.form["name"]
    genres = form_data.pop("genres")
    if isinstance(genres, str):
        genres = [genres]

    artist = Artist(**form_data)
    artist.genres = Genre.query.filter(Genre.name.in_(genres)).all()

    try:
        db.session.add(artist)
        db.session.commit()
        flash(f"Artist {artist_name} was successfully listed!")
    except:
        db.session.rollback()
        flash(f"An error occurred. Artist {artist_name} could not be listed.")

    return render_template("pages/home.html")


#  Shows
#  ----------------------------------------------------------------


@app.route("/shows")
def shows():
    shows_data = Show.query.all()
    shows_dict = [model_to_dict(show) for show in shows_data]
    return render_template("pages/shows.html", shows=shows_dict)


@app.route("/shows/create")
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template("forms/new_show.html", form=form)


@app.route("/shows/create", methods=["POST"])
def create_show_submission():
    form_data = request.form.to_dict()
    try:
        venue = Venue.query.filter_by(id=form_data['venue_id']).one()
    except exc.NoResultFound:
        raise exc.NoResultFound(f"No venue id = {form_data['venue_id']} was found].")

    try:
        artist = Artist.query.filter_by(id=form_data['artist_id']).one()
    except exc.NoResultFound:
        raise exc.NoResultFound(f"No artist id = {form_data['artist_id']} was found.'")

    data = {
        "venue_id": venue.id,
        "venue_name": venue.name,
        "venue_image_link": venue.image_link,
        "artist_id": artist.id,
        "artist_name": artist.name,
        "artist_image_link": artist.image_link,
        "start_time": parser.parse(form_data['start_time']).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    }

    show = Show(**data)

    # FIXME: primary key error
    try:
        db.session.add(show)
        db.session.commit()
        flash("Show was successfully listed!")
    except:
        db.session.rollback()
        flash('An error occurred. Show could not be listed.')

    return render_template("pages/home.html")


@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html"), 500


if not app.debug:
    file_handler = FileHandler("error.log")
    file_handler.setFormatter(
        Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info("errors")

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == "__main__":
    app.run()

# Or specify port manually:
"""
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
"""
