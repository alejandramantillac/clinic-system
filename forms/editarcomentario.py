from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, TextAreaField, HiddenField
from wtforms.fields.html5 import DateField,DateTimeField 
from wtforms.validators import DataRequired

class Editarcomentario(FlaskForm):

    comentariomedico = TextAreaField("Comentario Médico",  validators=[DataRequired()])

    guardar = SubmitField("Guardar")



    


    