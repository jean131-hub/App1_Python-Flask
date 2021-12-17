from flask import Flask
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
#Instalar mysql-client en entorno virtual
# para poder realizar consultas
mail = Mail()
db = SQLAlchemy()
bootstrap = Bootstrap()
csrf = CSRFProtect()
login_manager = LoginManager()

from .views import page
from .consts import LOGIN_REQUIRED
from .models import User, Task

def create_app(config):
    app.config.from_object(config)

    csrf.init_app(app)
    
    if not app.config.get('TEST', False):
        bootstrap.init_app(app)

    app.app_context().push()    #Lanzamos contexto de la aplicación, 
                                #asi corregir el error del los unitest

    login_manager.init_app(app)
    login_manager.login_view = '.login' #url_for
    login_manager.login_message = LOGIN_REQUIRED
    
    mail.init_app(app)

    app.register_blueprint(page)
                                                                 
    with app.app_context(): #Creamos un administrador de contexto.Nos permite administrar recursos
        db.init_app(app)
        db.create_all()                    
    
    return app