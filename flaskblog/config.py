import os

class Config:
    # SECRET_KEY = '78b81502f7e89045fe634e85d02f42c5'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    # MAIL_SERVER = 'smtp.gmail.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = 'flaskblog12345@gmail.com'
    # MAIL_PASSWORD = 'testerpw1'

    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USER')
    MAIL_PASSWORD = os.environ.get('MAIL_PW')

    # print(f'Mail username is:  {MAIL_USERNAME}')



