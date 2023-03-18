import os
from decouple import config
from datetime import timedelta




BASE_DIR = os.path.dirname(os.path.realpath(__file__))

db_name = 'sch_mgt.db'

default_uri = "postgres://{}:{}@{}/{}".format('postgres', 'password', 'localhost:5432', db_name)

uri = os.getenv('DATABASE_URL', default_uri)
if uri.startswith('postgres://'):
  uri = uri.replace('postgres://', 'postgresql://', 1)

class Config:
  SECRET_KEY = config('SECRET_KEY', 'my_secret_key😉')
  JWT_SECRET_KEY = config('JWT_SECRET_KEY', 'secret🔐')
  JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
  JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)




class Dev_config(Config):
  DEBUG = True
  SQLALCHEMY_ECHO = True
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(BASE_DIR, 'db.sqlite3')

class Test_config(Config):
  TESTING = True
  SQLALCHEMY_ECHO = True
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SQLALCHEMY_DATABASE_URI = 'sqlite://' 

class Prod_config(Config):
  SQLALCHEMY_DATABASE_URI = uri
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  DEBUG = config('DEBUG', False, cast=bool)




# Configuration Dictionary for representation
# --------------------------------------------
config_dict = {
  'dev': Dev_config,
  'test': Test_config,
  'prod': Prod_config
}
# ---------------------------------------------