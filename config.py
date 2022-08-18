import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Disable modification tracking system
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Connect to the database

# Database URI
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:chinecherem11@localhost:5432/fyyur'