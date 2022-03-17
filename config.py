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
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://ngnnquajwnmqkc:f373ffc30bcfcbe1e25a4705ac045b2caa75f5e2ab671f0e1dca3f7a281aa96c@ec2-3-222-204-187.compute-1.amazonaws.com:5432/d5269ncm85vh2m'


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
