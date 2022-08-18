# --------------------------------------------------------------------------- #
# Imports
# --------------------------------------------------------------------------- #

import sys 
import json
import babel
import logging
import dateutil.parser
from forms import *
from flask_wtf import Form
from flask_moment import Moment
from flask_migrate import Migrate
from models import db, Venue, Artist, Show
from logging import Formatter, FileHandler
from flask import Flask, render_template, request, flash, redirect, url_for


# --------------------------------------------------------------------------- #
# App Config.
# --------------------------------------------------------------------------- #

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)


# --------------------------------------------------------------------------- #
# Filters.
# --------------------------------------------------------------------------- #

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime


# --------------------------------------------------------------------------- #
# Controllers.
# --------------------------------------------------------------------------- #
# Homepage ------------------------------------------------------------------ #

@app.route('/')
def index():
  venues = Venue.query.order_by(db.desc(Venue.created_at)).limit(10).all()
  artists = Artist.query.order_by(db.desc(Artist.created_at)).limit(10).all()
  return render_template('pages/home.html', venues=venues, artists=artists)


# All Venues ---------------------------------------------------------------- #

@app.route('/venues')
def venues():
  data=[]
  distinct_locations = Venue.query.with_entities(Venue.city, Venue.state).distinct().all()

  for location in distinct_locations:
    venues = Venue.query.filter_by(city=location.city, state=location.state).all()
    modified_venues = []
    for venue in venues:
      modified_venues.append({
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": Show.query.filter_by(venue_id=venue.id).filter(Show.start_time > datetime.now()).count()
      })

    data.append({
      "city": location.city,
      "state": location.state,
      "venues": modified_venues,
    })

  return render_template('pages/venues.html', areas=data)


# Create Venue -------------------------------------------------------------- #

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm(request.form)
  if form.validate():
    try:
      new_venue = Venue(
        name=form.name.data,
        city=form.city.data,
        state=form.state.data,
        address=form.address.data,
        phone=form.phone.data,
        genres=form.genres.data,
        facebook_link=form.facebook_link.data,
        image_link=form.image_link.data,
        website=form.website_link.data,
        seeking_talent=form.seeking_talent.data,
        seeking_description=form.seeking_description.data
      )
      db.session.add(new_venue)
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
      db.session.rollback()
      print(sys.exc_info())
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    finally:
      db.session.close()
  else:
    print('Form errors: ', form.errors)
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')

  return redirect(url_for("index"))


# Search Venue -------------------------------------------------------------- #

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term', '')
  venues = Venue.query.filter(
    Venue.name.ilike(f'%{search_term}%') | 
    Venue.city.ilike(f'%{search_term}%') |
    Venue.state.ilike(f'%{search_term}%')
    ).all()

  data = []
  for venue in venues:
    data.append({
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": Show.query.filter_by(venue_id=venue.id).filter(Show.start_time > datetime.now()).count()
    })

  response = {
    "count": len(venues),
    "data": data
  }
  
  return render_template('pages/search_venues.html', results=response, search_term=search_term)


# View Venue ---------------------------------------------------------------- #

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.get(venue_id)
  modified_past_shows = []
  past_shows = Show.query.filter_by(venue_id=venue_id).filter(Show.start_time < datetime.now()).all()
  for show in past_shows:
    modified_past_shows.append({
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
    })
  
  modified_upcoming_shows = []
  upcoming_shows = Show.query.filter_by(venue_id=venue_id).filter(Show.start_time > datetime.now()).all()
  for show in upcoming_shows:
    modified_upcoming_shows.append({
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
    })

  venue.past_shows = modified_past_shows
  venue.upcoming_shows = modified_upcoming_shows
  venue.past_shows_count = len(past_shows)
  venue.upcoming_shows_count = len(upcoming_shows)

  return render_template('pages/show_venue.html', venue=venue)


# Edit Venue - GET ---------------------------------------------------------- #

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  form.name.data = venue.name
  form.genres.data = venue.genres
  form.address.data = venue.address
  form.city.data = venue.city
  form.state.data = venue.state
  form.phone.data = venue.phone
  form.website_link.data = venue.website
  form.facebook_link.data = venue.facebook_link
  form.seeking_talent.data = venue.seeking_talent
  form.seeking_description.data = venue.seeking_description
  form.image_link.data = venue.image_link

  return render_template('forms/edit_venue.html', form=form, venue=venue)


# Edit Venue - POST --------------------------------------------------------- #

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  form = VenueForm(request.form)
  if form.validate():
    try:
      venue = Venue.query.get(venue_id)
      venue.name = form.name.data
      venue.city = form.city.data
      venue.state = form.state.data
      venue.address = form.address.data
      venue.phone = form.phone.data
      venue.genres = form.genres.data
      venue.facebook_link = form.facebook_link.data
      venue.image_link = form.image_link.data
      venue.website = form.website_link.data
      venue.seeking_talent = form.seeking_talent.data
      venue.seeking_description = form.seeking_description.data
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully updated!')
    except:
      db.session.rollback()
      print(sys.exc_info())
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')
    finally:
      db.session.close()
  else:
    print('Form errors: ', form.errors)
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')

  return redirect(url_for('show_venue', venue_id=venue_id))


# Delete Venue -------------------------------------------------------------- #

@app.route('/venues/<venue_id>/delete', methods=['GET'])
def delete_venue(venue_id):
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
    flash('Venue ' + venue.name + ' was successfully deleted!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Venue ' + venue.name + ' could not be deleted.')
  finally:
    db.session.close()

  return redirect(url_for("index"))


# All Artists --------------------------------------------------------------- #

@app.route('/artists')
def artists():
  data=[]
  artists = Artist.query.all()

  for artist in artists:
    data.append({
      "id": artist.id,
      "name": artist.name
    })

  return render_template('pages/artists.html', artists=data)


# Create Artist ------------------------------------------------------------- #

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm(request.form)
  if form.validate():
    try:
      new_artist = Artist(
        name=form.name.data,
        city=form.city.data,
        state=form.state.data,
        phone=form.phone.data,
        genres=form.genres.data,
        facebook_link=form.facebook_link.data,
        image_link=form.image_link.data,
        website=form.website_link.data,
        seeking_venue=form.seeking_venue.data,
        seeking_description=form.seeking_description.data
      )
      db.session.add(new_artist)
      db.session.commit()
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
      db.session.rollback()
      print(sys.exc_info())
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    finally:
      db.session.close()
  else:
    print('Form errors: ', form.errors)
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')

  return redirect(url_for("index"))


# Search Artist ------------------------------------------------------------- #

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term', '')
  artists = Artist.query.filter(
    Artist.name.ilike(f'%{search_term}%') | 
    Artist.city.ilike(f'%{search_term}%') |
    Artist.state.ilike(f'%{search_term}%')
    ).all()

  data = []
  for artist in artists:
    data.append({
      "id": artist.id,
      "name": artist.name,
      "num_upcoming_shows": Show.query.filter_by(artist_id=artist.id).filter(Show.start_time > datetime.now()).count()
    })
    
  response = {
    "count": len(artists),
    "data": data
  }
  
  return render_template('pages/search_venues.html', results=response, search_term=search_term)


# View Artist --------------------------------------------------------------- #

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)
  modified_past_shows = []
  past_shows = Show.query.filter_by(artist_id=artist_id).filter(Show.start_time < datetime.now()).all()
  for show in past_shows:
    modified_past_shows.append({
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "venue_image_link": show.venue.image_link,
      "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
    })
  
  modified_upcoming_shows = []
  upcoming_shows = Show.query.filter_by(artist_id=artist_id).filter(Show.start_time > datetime.now()).all()
  for show in upcoming_shows:
    modified_upcoming_shows.append({
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "venue_image_link": show.venue.image_link,
      "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
    })

  artist.past_shows = modified_past_shows
  artist.upcoming_shows = modified_upcoming_shows
  artist.past_shows_count = len(past_shows)
  artist.upcoming_shows_count = len(upcoming_shows)

  return render_template('pages/show_artist.html', artist=artist)


# Edit Artist - GET --------------------------------------------------------- #

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  form.name.data = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.genres.data = artist.genres
  form.facebook_link.data = artist.facebook_link
  form.image_link.data = artist.image_link
  form.website_link.data = artist.website
  form.seeking_venue.data = artist.seeking_venue
  form.seeking_description.data = artist.seeking_description

  return render_template('forms/edit_artist.html', form=form, artist=artist)


# Edit Artist - POST -------------------------------------------------------- #

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  form = ArtistForm(request.form)
  if form.validate():
    try:
      artist = Artist.query.get(artist_id)
      artist.name = form.name.data
      artist.city = form.city.data
      artist.state = form.state.data
      artist.phone = form.phone.data
      artist.genres = form.genres.data
      artist.facebook_link = form.facebook_link.data
      artist.image_link = form.image_link.data
      artist.website = form.website_link.data
      artist.seeking_venue = form.seeking_venue.data
      artist.seeking_description = form.seeking_description.data
      db.session.commit()
      flash('Artist ' + request.form['name'] + ' was successfully updated!')
    except:
      db.session.rollback()
      print(sys.exc_info())
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')
    finally:
      db.session.close()
  else:
    print('Form errors: ', form.errors)
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')

  return redirect(url_for('show_artist', artist_id=artist_id))


# Delete Artist ------------------------------------------------------------- #

@app.route('/artists/<artist_id>/delete', methods=['GET'])
def delete_artist(artist_id):
  try:
    artist = Artist.query.get(artist_id)
    db.session.delete(artist)
    db.session.commit()
    flash('Artist ' + artist.name + ' was successfully deleted!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Artist ' + artist.name + ' could not be deleted.')
  finally:
    db.session.close()

  return redirect(url_for("index"))


# All Shows ----------------------------------------------------------------- #

@app.route('/shows')
def shows():
  data = []
  shows = Show.query.all()
  for show in shows:
    data.append({
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
    })

  return render_template('pages/shows.html', shows=data)


# Create Show --------------------------------------------------------------- #

@app.route('/shows/create')
def create_shows():
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  form = ShowForm(request.form)
  if form.validate():
    try:
      new_show = Show(
        venue_id=form.venue_id.data,
        artist_id=form.artist_id.data,
        start_time=form.start_time.data,
      )
      db.session.add(new_show)
      db.session.commit()
      flash('Show was successfully listed!')
    except:
      db.session.rollback()
      print(sys.exc_info())
      flash('An error occurred. Show could not be listed.')
    finally:
      db.session.close()
  else:
    print('Form errors: ', form.errors)
    flash('An error occurred. Show could not be listed.')

  return redirect(url_for("index"))


# --------------------------------------------------------------------------- #
# Error Handlers
# --------------------------------------------------------------------------- #
# Page Not Found ------------------------------------------------------------ #

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


# Server Error -------------------------------------------------------------- #

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500
    

# Error Logger -------------------------------------------------------------- #

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')
    

#-----------------------------------------------------------------------------#
# Launch
#-----------------------------------------------------------------------------#
# Default port -------------------------------------------------------------- #

if __name__ == '__main__':
    app.run()


# Manual Port --------------------------------------------------------------- #
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
