from decouple import config #'''Decouple me permite trabajar 
                            #con variables de entorno'''

class Config:
    SECRET_KEY = 'C@racoltv50'
    
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:JDmartinez97#@localhost/project_web_flask'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'jeanmartinez22782@gmail.com'
    MAIL_PASSWORD = config('MAIL_PASSWORD') #Variable de entorno
                                                                     
config = {
    'development':DevelopmentConfig,
    'default':DevelopmentConfig
}

