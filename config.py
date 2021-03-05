import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
SQLALCHEMY_TRACK_MODIFICATIONS = False
#SQLALCHEMY_DATABASE_URI = 'postgres://postgres:123456@localhost:5432/capstone'
SQLALCHEMY_DATABASE_URI = 'postgres://wmdxdhgvjanseg:f2f9741943d1e87b9e9362ec0a8326ff08266e97a46bc6e5511a5aea0c655805@ec2-54-145-249-177.compute-1.amazonaws.com:5432/d35f5a2pd91il5'
