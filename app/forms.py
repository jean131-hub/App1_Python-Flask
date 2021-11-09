from wtforms import Form
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms import HiddenField
from wtforms.fields.html5 import EmailField
from wtforms import validators

from .models import User

def codi_validator(form, field):
    if field.data == 'codi' or field.data == 'Codi':
        raise validators.ValidationError('El username {} no es permitido.'.format(field.data))

def length_honeypot(form, field):
    if len(field.data) > 0:
        raise validators.ValidationError('Solo pueden llenar este formulario humanos!')

class LoginForm(Form):
    username = StringField('Username', [
        validators.length(min=4, max=50)
    ])
    password = PasswordField('Password', [
        validators.Required(message='Por favor llene este campo.')
    ])

class RegisterForm(Form):

    username = StringField('Username', [
        validators.length(min=4, max=50),
        codi_validator
    ])

    email = EmailField('Email', [
        validators.length(min=6, max=100),
        validators.Required(message='El email es requerido.'),
        validators.Email(message='Ingrese email válido')
    ])

    password = PasswordField('Password', [
        validators.Required(message='El password es requerido'),
        validators.EqualTo('confirm_password',
                           message='La contraseña no coincide.'),
    ])
    
    confirm_password = PasswordField('Confirm password')

    accept = BooleanField('Acepto términos y condiciones', [
        validators.DataRequired()
    ])

    honeypot = HiddenField("", [length_honeypot])

    def validate_username(self, username):
        if User.get_by_username(username.data):
            raise validators.ValidationError('El username {} ya se encuentra en uso.'.format(username.data))

    def validate_email(self, email):
        if User.get_by_email(email.data):
            raise validators.ValidationError('El email ya se encuentra en uso.')

    #Se sobrescribe el metodo validate de la clase Form
    def validate(self):
        if not Form.validate(self): #Se ejecutan todas las validaciones antes de sobrescribir
            return False
        if len(self.password.data) < 3: #Se sobrescribe, añadiendo validaciones
            self.password.errors.append('La contraseña es demasiado corta.')
            return False
        return True

class TaskForm(Form):
    title = StringField('Título', [
        validators.length(min=4, max=50, message='Título fuera de rango.'),
        validators.DataRequired(message='El título es requerido')
    ])

    description = TextAreaField('Descripción', [
        validators.DataRequired('La descripción es requerida'), 
    ], render_kw={'rows': 5})