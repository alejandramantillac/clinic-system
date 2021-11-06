from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, BooleanField
from wtforms.fields.html5 import DateField,DateTimeField 
from wtforms.validators import DataRequired

class Calificar(FlaskForm):

     calificacion = SelectField ("Calificar Atención", choices=[('0', ''), ('1', 'Muy Malo'), ('2', 'Malo'), ('3', 'Regular'), ('4', 'Bueno'), ('5', 'Excelente')]) 

     calificar = SubmitField("Calificar")  
    