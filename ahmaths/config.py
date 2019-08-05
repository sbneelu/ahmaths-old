import json
import os

with open('config.json', 'r') as f:
    config_file = f.read()
    config = json.loads(config_file)


class Config:
    SECRET_KEY = config['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = config['SQLALCHEMY_DATABASE_URI']
    MAIL_SERVER = config['MAIL_SERVER']
    MAIL_PORT = config['MAIL_PORT']
    MAIL_USE_TLS = config['MAIL_USE_TLS']
    MAIL_USERNAME = os.environ.get('APP_TESTING_EMAIL')
    MAIL_PASSWORD = os.environ.get('APP_TESTING_EMAIL_PASSWORD')
