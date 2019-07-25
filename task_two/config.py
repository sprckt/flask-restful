import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    path_to_db = os.path.join(os.getcwd(), 'nest.db')
    print(f'DB path: {path_to_db}')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path_to_db
    SQLALCHEMY_TRACK_MODIFICATIONS = False

