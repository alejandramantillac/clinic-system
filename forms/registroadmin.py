from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.fields.html5 import DateField,DateTimeField, EmailField 
from wtforms.validators import DataRequired

class Registroadmin(FlaskForm):

    
    tipodocumento = SelectField ("Tipo De Documento", choices=[('0', ''), ('Cedula De Ciudadania', 'Cedula De Ciudadania'), ('Tarjeta De Identidad', 'Tarjeta De Identidad'), ('Cedula De Extranjería', 'Cedula De Extranjería')]) 
    
    numerodocumento = IntegerField("Número De Documento", validators=[DataRequired()])

    nombre = StringField("Nombre",  validators=[DataRequired()])
    
    correo = EmailField("Correo", validators=[DataRequired()])
    
    fechanacimiento  = DateField('Fecha De Nacimiento ', format='%Y-%m-%d')
   
    genero = SelectField ("Genero", choices=[('0', ''), ('Masculino', 'Masculino'), ('Femenino', 'Femenino')])

    direccion = StringField("Dirección", validators=[DataRequired()]) 

    telefono = IntegerField("Teléfono", validators=[DataRequired()])

    contrasena = PasswordField("Contraseña", validators=[DataRequired()])

    cargo = SelectField ("Cargo", choices=[('0', ''), ('Diseño', 'Diseño'), ('Mantenimiento', 'Mantenimiento'), ('Supervisor', 'Supervisor')]) 
    enviar = SubmitField("Registrar")


    