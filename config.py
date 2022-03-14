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
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://james:password@localhost/myblog_test'


class ProdConfig(Config):
    '''
Production  configuration child class

Args:
    Config: The parent configuration class with General configuration settings
'''
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://fbohtwdnvfhgny:070c1842edff64c8eb7002afefb02c40e52840dcd93579b20c472cf72a067849@ec2-52-44-209-165.compute-1.amazonaws.com:5432/d34993vdvhpf6o'


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
