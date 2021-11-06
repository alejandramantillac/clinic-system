from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, TextAreaField, HiddenField
from wtforms.fields.html5 import TimeField
from wtforms.validators import DataRequired

class Nuevaconsulta(FlaskForm): 

    id_cita = HiddenField()

   
    #hora =TimeField('Hora')
    hora = StringField("Hora",  validators=[DataRequired()])

    peso = StringField("Peso",  validators=[DataRequired()])

    estatura = StringField("Estatura",  validators=[DataRequired()])

    ocupacion = StringField("Ocupación",  validators=[DataRequired()])

    motivoconsulta = StringField("Motivo De Consulta",  validators=[DataRequired()])

    diagnostico = TextAreaField("Diagnostico",  validators=[DataRequired()])

    comentariomedico = TextAreaField("Comentario Médico",  validators=[DataRequired()])

    guardar = SubmitField("Guardar")



    

