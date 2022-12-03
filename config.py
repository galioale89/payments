import os

SECRET_KEY = 'mekal'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{user}:{password}@{server}/{database}'.format(
        SGBD = 'mysql',
        user = 'root',
        password = '64l10770',
        server = 'localhost',
        database = 'mekal'
    )