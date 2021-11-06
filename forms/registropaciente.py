from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.fields.html5 import DateField,EmailField 
from wtforms.validators import DataRequired

class Registropaciente(FlaskForm):

    

    tipodocumento = SelectField ("Tipo De Documento: *", choices=[('0', ''), ('Cedula De Ciudadania', 'Cedula De Ciudadania'), ('Tarjeta De Identidad', 'Tarjeta De Identidad'), ('Cedula De Extranjería', 'Cedula De Extranjería')]) 
    
    numerodocumento = IntegerField("Número De Documento: *", validators=[DataRequired()])

    nombre = StringField("Nombres y Apellidos: *",  validators=[DataRequired()])
    
    correo = EmailField("Correo: *", validators=[DataRequired()])
    
    fechanacimiento  = DateField('Fecha De Nacimiento: * ', format='%Y-%m-%d')
   
    genero = SelectField ("Género: *", choices=[('0', ''), ('Masculino', 'Masculino'), ('Femenino', 'Femenino'), ('No binario', 'No binario')])

    direccion = StringField("Dirección: *", validators=[DataRequired()]) 

    telefono = IntegerField("Teléfono: *", validators=[DataRequired()])

    contrasena = PasswordField("Contraseña:* ", validators=[DataRequired()])

    eps = StringField("EPS: *", validators=[DataRequired()])
    
    enviar = SubmitField("Registrar")
    


    