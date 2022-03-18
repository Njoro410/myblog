from distutils.debug import DEBUG
import os


class Config:
    """_General configuration parent class
    """
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://brian:12345@localhost/myblog'
    UPLOADED_PHOTOS_DEST = 'app/static/photos'
    MAIL_USERNAME = os.environ.get('EMAIL_ADDRESS')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://brian:12345@localhost/myblog_test'


class ProdConfig(Config):
    '''
Production  configuration child class

Args:
    Config: The parent configuration class with General configuration settings
'''
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://pnbdxymtuwxjnd:fbf57888dc8e2148dc772238e5842b750d13b2ec574627b4d21285b4ba5f6652@ec2-44-194-69-15.compute-1.amazonaws.com:5432/df6g1utl982icu'


class DevConfig(Config):
    '''
Development  configuration child class

Args:
    Config: The parent configuration class with General configuration settings
'''
    DEBUG = True


config_options = {
    'development': DevConfig,
    'production': ProdConfig,
    'test': TestConfig
}
