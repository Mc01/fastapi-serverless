from os import environ


FAUNADB_SECRET = environ.get('FAUNADB_SECRET')
FAUNADB_DBNAME = environ.get('FAUNADB_DBNAME', default='fastapi')
TIMEZONE = environ.get('TIMEZONE', default='Europe/Warsaw')
