from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.fields.html5 import DateField,DateTimeField 
from wtforms.validators import DataRequired

class Solicitarcita(FlaskForm):

    
    nombre = StringField("Nombre") 
    
    fecha = DateField('Fecha ', format='%Y-%m-%d')
   
    especialidad = SelectField ("Especialidad", choices=[('0', ''), ('Medicina General', 'Medicina General'), ('Pediatría', 'Pediatría'), ('Medicina Interna', 'Medicina Interna')])
    
  
    buscar = SubmitField("Buscar")
    


    