from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.fields.html5 import DateField,DateTimeField 
from wtforms.validators import DataRequired

class Crearcitas(FlaskForm):

    
    
    fecha = DateField('Fecha ', format='%Y-%m-%d')
   
    

    direccion = StringField("Dirección", validators=[DataRequired()]) 

   
    
    crear = SubmitField("Crear Cita")
    


    