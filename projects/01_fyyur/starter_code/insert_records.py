from app import Artist, Genre, Show, Venue, db


def insert_genres():
    genres = {
        "Jazz",
        "Reggae",
        "Swing",
        "Classical",
        "Folk",
        "R&B",
        "Hip-Hop",
        "Rock n Roll",
    }
    objects = [Genre(name=genre) for genre in genres]

    db.session.bulk_save_objects(objects)
    db.session.commit()


def insert_shows():
    show_1 = Show(
        venue_id=1,
        venue_name="The Musical Hop",
        venue_image_link="https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
        artist_id=4,
        artist_name="Guns N Petals",
        artist_image_link="https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        start_time="2019-05-21T21:30:00.000Z",
    )

    show_2 = Show(
        venue_id=3,
        venue_name="Park Square Live Music & Coffee",
        venue_image_link="https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
        artist_id=5,
        artist_name="Matt Quevedo",
        artist_image_link="https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
        start_time="2019-06-15T23:00:00.000Z",
    )

    show_3 = Show(
        venue_id=3,
        venue_name="Park Square Live Music & Coffee",
        venue_image_link="https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
        artist_id=6,
        artist_name="The Wild Sax Band",
        artist_image_link="https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        start_time="2035-04-01T20:00:00.000Z",
    )

    show_4 = Show(
        venue_id=3,
        venue_name="Park Square Live Music & Coffee",
        venue_image_link="https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
        artist_id=6,
        artist_name="The Wild Sax Band",
        artist_image_link="https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        start_time="2035-04-08T20:00:00.000Z",
    )

    show_5 = Show(
        venue_id=3,
        venue_name="Park Square Live Music & Coffee",
        venue_image_link="https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
        artist_id=6,
        artist_name="The Wild Sax Band",
        artist_image_link="https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        start_time="2035-04-15T20:00:00.000Z",
    )

    db.session.add_all([show_1, show_2, show_3, show_4, show_5])
    db.session.commit()


def insert_venues():
    venue_1 = Venue(
        id=1,
        name="The Musical Hop",
        city="San Francisco",
        state="CA",
        address="1015 Folsom Street",
        phone="123-123-1234",
        image_link="https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
        facebook_link="https://www.facebook.com/TheMusicalHop",
        website="https://www.themusicalhop.com",
        seeking_talent=True,
        seeking_description="We are on the lookout for a local artist to play every two weeks. Please call us.",
    )

    venue_2 = Venue(
        id=2,
        name="The Dueling Pianos Bar",
        city="New York",
        state="NY",
        address="335 Delancey Street",
        phone="914-003-1132",
        image_link="https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
        facebook_link="https://www.facebook.com/theduelingpianos",
        website="https://www.theduelingpianos.com",
        seeking_talent=False,
    )

    venue_3 = Venue(
        id=3,
        name="Park Square Live Music & Coffee",
        city="San Francisco",
        state="CA",
        address="34 Whiskey Moore Ave",
        phone="415-000-1234",
        image_link="https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
        facebook_link="https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
        website="https://www.parksquarelivemusicandcoffee.com",
        seeking_talent=False,
    )

    db.session.add_all([venue_1, venue_2, venue_3])
    db.session.commit()


def insert_artists():
    artist_1 = Artist(
        id=4,
        name="Guns N Petals",
        city="San Francisco",
        state="CA",
        phone="326-123-5000",
        website="https://www.gunsnpetalsband.com",
        image_link="https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        facebook_link="https://www.facebook.com/GunsNPetals",
        seeking_venue=True,
        seeking_description="Looking for shows to perform at in the San Francisco Bay Area!",
    )

    artist_2 = Artist(
        id=5,
        name="Matt Quevedo",
        city="New York",
        state="NY",
        phone="300-400-5000",
        image_link="https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
        facebook_link="https://www.facebook.com/mattquevedo923251523",
        seeking_venue=False,
    )

    artist_3 = Artist(
        id=6,
        name="The Wild Sax Band",
        city="San Francisco",
        state="CA",
        phone="432-325-5432",
        image_link="https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        facebook_link="https://www.facebook.com/mattquevedo923251523",
        seeking_venue=False,
    )

    db.session.add_all([artist_1, artist_2, artist_3])
    db.session.commit()


def add_venue_genres_relationships():
    venue_1 = Venue.query.filter_by(id=1).one()
    venue_1.genres = Genre.query.filter(
        Genre.name.in_(["Jazz", "Reggae", "Swing", "Classical", "Folk"])
    ).all()

    venue_2 = Venue.query.filter_by(id=2).one()
    venue_2.genres = Genre.query.filter(
        Genre.name.in_(["Classical", "R&B", "Hip-Hop"])
    ).all()

    venue_3 = Venue.query.filter_by(id=1).one()
    venue_3.genres = Genre.query.filter(
        Genre.name.in_(["Rock n Roll", "Jazz", "Classical", "Folk"])
    ).all()

    db.session.add_all([venue_1, venue_2, venue_3])
    db.session.commit()


def add_artist_genres_relationships():
    artist_1 = Artist.query.filter_by(id=4).one()
    artist_1.genres = Genre.query.filter(Genre.name.in_(["Rock n Roll"])).all()

    artist_2 = Artist.query.filter_by(id=5).one()
    artist_2.genres = Genre.query.filter(Genre.name.in_(["Jazz"])).all()

    artist_3 = Artist.query.filter_by(id=6).one()
    artist_3.genres = Genre.query.filter(Genre.name.in_(["Jazz", "Classical"])).all()

    db.session.add_all([artist_1, artist_2, artist_3])
    db.session.commit()


def add_venue_show_relationships():
    venue_1 = Venue.query.filter_by(id=1).one()
    venue_1.shows = Show.query.filter_by(venue_id=1).all()

    venue_2 = Venue.query.filter_by(id=2).one()
    venue_2.shows = []

    venue_3 = Venue.query.filter_by(id=3).one()
    venue_3.shows = Show.query.filter_by(venue_id=3).all()

    db.session.add_all([venue_1, venue_2, venue_3])
    db.session.commit()


def add_artist_show_relationships():
    artist_4 = Artist.query.filter_by(id=4).one()
    artist_4.shows = Show.query.filter_by(artist_id=4).all()

    artist_5 = Artist.query.filter_by(id=5).one()
    artist_5.shows = Show.query.filter_by(artist_id=5).all()

    artist_6 = Artist.query.filter_by(id=6).one()
    artist_6.shows = Show.query.filter_by(artist_id=6).all()

    db.session.add_all([artist_4, artist_5, artist_6])
    db.session.commit()


if __name__ == "__main__":
    insert_genres()  # done
    insert_venues()  # done
    insert_artists()  # done
    insert_shows()  # done

    add_venue_genres_relationships()  # done
    add_artist_genres_relationships()  # done
    add_venue_show_relationships()  # done
    add_artist_show_relationships  # done

# Nuke postgres tables
# truncate artist, artist_and_genre, genre, show, venue, venue_and_genre cascade;
