from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, BooleanField
from wtforms.fields.html5 import DateField,DateTimeField 
from wtforms.validators import DataRequired

class Login(FlaskForm):

    tipousuario = SelectField ("Tipo De Usuario: *", choices=[('0', ''), ('Paciente', 'Paciente'), ('Medico', 'Médico'), ('Administrador', 'Administrador')]) 

    correo = StringField("Correo: *", validators=[DataRequired()])
    
    contrasena = PasswordField("Contraseña: *", validators=[DataRequired()])

    iniciarsesion = SubmitField("Iniciar Sesión")  
    