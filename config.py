from distutils.debug import DEBUG
import os


class Config:
    """_General configuration parent class
    """
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://brian:12345@localhost/myblog'
    UPLOADED_PHOTOS_DEST ='app/static/photos'
    
class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://james:password@localhost/myblog_test'


class ProdConfig(Config):
        '''
    Production  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
        pass

class DevConfig(Config):
        '''
    Development  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
        DEBUG = True
    
config_options = {
    'development': DevConfig,
    'production':ProdConfig,
    'test':TestConfig
}