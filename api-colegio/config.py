import os

class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'colegio_porto.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'porto-secreto-2025'