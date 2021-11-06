from flask import Flask, session, flash
from flask.scaffold import F
from flask import render_template 
from flask import redirect
from flask import request
import sqlite3
import os
from wtforms.compat import with_metaclass
import hashlib
from forms.registropaciente import Registropaciente
from forms.registromedico import Registromedico
from forms.registroadmin import Registroadmin  
from forms.crearcitas import Crearcitas
from forms.login import Login
from forms.calificaratencion import Calificar
from forms.nuevaconsulta import Nuevaconsulta
from forms.solicitarcita import Solicitarcita
from forms.editarcomentario import Editarcomentario
from forms.actualizardatospaciente import Actualizardatospaciente
from forms.actualizardatosmedico import Actualizardatosmedico
from werkzeug.utils import escape




app = Flask(__name__)

app.secret_key = os.urandom(20)




#pagina inicio------------------------------------------------------------------

@app.route('/', methods=["Get"])

def home():
    return  render_template ("index.html")


#pagina login-----------------------------------------------------------------------------

@app.route('/login', methods=["Get","POST"])
def login():
    frm = Login()
    mensaje = ""
    if frm.validate_on_submit():
        tipousuario = frm.tipousuario.data
        correo = escape(frm.correo.data) #limpiar quita instrucciones maliciosas
        contrasena = escape(frm.contrasena.data)
         # Cifra la contraseña
        encrp = hashlib.sha256(contrasena.encode('utf-8'))
        pass_enc = encrp.hexdigest()
        with sqlite3.connect("clinica.db") as con: 
            cur = con.cursor()
            cur.execute(
                "SELECT * FROM usuario WHERE tipousuario = ? AND correo = ? AND contrasena = ?", [tipousuario, correo, pass_enc])

            rows = cur.fetchall()
            if len(rows) > 0:

                for usu in rows:
                    session["id_usuario"] = usu[0]
                    session["tipousuario"] = usu[1]
                    session["nombre"] = usu[4]
                    

                if  session["tipousuario"] == "Paciente":

                        return redirect("/perfil_usuario_paciente")

                elif session["tipousuario"] == "Medico":
            
                        return redirect("/perfil_usuario_medico")    

                elif session["tipousuario"] == "Administrador":

                        return redirect("/perfil_admin")
           
           
           
            else:
                mensaje = "Correo/Contraseña incorrectos"    
    

    return render_template("login.html", frm=frm,mensaje= mensaje )




#cerrar sesion------------------------------------------------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")            


# registro Paciente----------------------------------------------------------------------

@app.route('/registropaciente', methods=["GET","POST"])
def registrar():
    frm = Registropaciente()
    mensaje = ""
    if frm.validate_on_submit():
        if frm.enviar:
            
            tipodocumento = frm.tipodocumento.data
            numerodocumento = frm.numerodocumento.data
            nombre = frm.nombre.data
            correo = frm.correo.data
            fechanacimiento = frm.fechanacimiento.data
            genero = frm.genero.data
            direccion = frm.direccion.data
            telefono = frm.telefono.data
            contrasena = frm.contrasena.data
            eps = frm.eps.data
              
            # Cifra la contraseña
            encrp = hashlib.sha256(contrasena.encode('utf-8'))
            pass_enc = encrp.hexdigest()
            # Conecta a la BD
            with sqlite3.connect("clinica.db") as con:
                # Crea un cursor para manipular la BD
                cur = con.cursor()
                # Prepara la sentencia SQL
                
                cur.execute("INSERT INTO usuario ( tipousuario, tipodocumento, numerodocumento,  nombre, correo, fechanacimiento, genero, direccion, telefono, contrasena ) VALUES (?,?,?,?,?,?,?,?,?,?)", ["Paciente", tipodocumento, numerodocumento,  nombre, correo, fechanacimiento, genero, direccion, telefono, pass_enc])
                           
                # Ejecuta la sentencia SQL

                con.commit()

               

                cur.execute("SELECT * FROM usuario WHERE numerodocumento = ?", [numerodocumento])

                rows = cur.fetchall()
                id_usuario = 0

                for usu in rows:
                    id_usuario =  usu[0]

                
                #cur = con.cursor()
                cur.execute("INSERT INTO paciente ( id_paciente, eps ) VALUES (?,?)", [
                            id_usuario, eps])

                con.commit()
                mensaje = "Registrado con exito"  

    return render_template("registropaciente.html", frm=frm,mensaje = mensaje)

    


# registro medico--------------------------------------------------------------------------------------------------------

@app.route('/registromedico', methods=["GET","POST"])
def registrarmedico():
    frm = Registromedico()
    mensaje = ""
    if 'tipousuario' in session:
            if session["tipousuario"] ==  'Administrador' :

                if frm.validate_on_submit():
                    if frm.enviar:
                        
                        tipodocumento = frm.tipodocumento.data
                        numerodocumento = frm.numerodocumento.data
                        nombre = frm.nombre.data
                        correo = frm.correo.data
                        fechanacimiento = frm.fechanacimiento.data
                        genero = frm.genero.data
                        direccion = frm.direccion.data
                        telefono = frm.telefono.data
                        contrasena = frm.contrasena.data
                        especialidad = frm.especialidad.data
                        numeroregistro = frm.numeroregistro.data
                        
                        # Cifra la contraseña
                        encrp = hashlib.sha256(contrasena.encode('utf-8'))
                        pass_enc = encrp.hexdigest()
                        # Conecta a la BD
                        with sqlite3.connect("clinica.db") as con:
                            # Crea un cursor para manipular la BD
                            cur = con.cursor()
                            # Prepara la sentencia SQL
                            cur.execute("INSERT INTO usuario ( tipousuario, tipodocumento, numerodocumento,  nombre, correo, fechanacimiento, genero, direccion, telefono, contrasena ) VALUES (?,?,?,?,?,?,?,?,?,?)", [ "Medico", tipodocumento, numerodocumento,  nombre, correo, fechanacimiento, genero, direccion, telefono, pass_enc])
                                    
                            # Ejecuta la sentencia SQL


                            con.commit()

                            cur.execute("SELECT * FROM usuario WHERE numerodocumento = ?", [numerodocumento])

                            rows = cur.fetchall()
                            id_usuario = 0

                            for usu in rows:
                                id_usuario =  usu[0]

                            
                            #cur = con.cursor()
                            cur.execute("INSERT INTO medico ( id_medico, especialidad, numeroregistro ) VALUES (?,?,?)", [
                                        id_usuario, especialidad, numeroregistro])

                            con.commit()
                            mensaje = "Usuario Médico registrado con exito"  

            else:
                frm = Login()
                mensaje = "La página que desea acceder no esta disponible"
                return render_template("login.html", frm=frm,mensaje=mensaje)

    else:
        frm = Login()
        mensaje = "La página que desea acceder no esta disponible"
        return render_template("login.html", frm=frm,mensaje=mensaje)                
               

    return render_template("registromedico.html", frm = frm, mensaje = mensaje )



# registro admin---------------------------------------------------------------------------------------------------------------

@app.route('/registroadmin', methods=["GET","POST"])
def registraradmin():
    frm = Registroadmin()
    mensaje = ""
    if 'tipousuario' in session:
            if session["tipousuario"] ==  'Administrador' :

                if frm.validate_on_submit():
                    if frm.enviar:
                        tipodocumento = frm.tipodocumento.data
                        numerodocumento = frm.numerodocumento.data
                        nombre = frm.nombre.data
                        correo = frm.correo.data
                        fechanacimiento = frm.fechanacimiento.data
                        genero = frm.genero.data
                        direccion = frm.direccion.data
                        telefono = frm.telefono.data
                        contrasena = frm.contrasena.data
                        cargo = frm.cargo.data
                        
                        
                        # Cifra la contraseña
                        encrp = hashlib.sha256(contrasena.encode('utf-8'))
                        pass_enc = encrp.hexdigest()
                        # Conecta a la BD
                        with sqlite3.connect("clinica.db") as con:
                            # Crea un cursor para manipular la BD
                            cur = con.cursor()
                            # Prepara la sentencia SQL
                            cur.execute("INSERT INTO usuario ( tipousuario, tipodocumento, numerodocumento,  nombre, correo, fechanacimiento, genero, direccion, telefono, contrasena ) VALUES (?,?,?,?,?,?,?,?,?,?)", [ "Administrador", tipodocumento, numerodocumento,  nombre, correo, fechanacimiento, genero, direccion, telefono, pass_enc])
                                    
                            # Ejecuta la sentencia SQL


                            con.commit()

                            cur.execute("SELECT * FROM usuario WHERE numerodocumento = ?", [numerodocumento])

                            rows = cur.fetchall()
                            id_usuario = 0

                            for usu in rows:
                                id_usuario =  usu[0]

                            
                            #cur = con.cursor()
                            cur.execute("INSERT INTO administrador ( id_administrador, cargo ) VALUES (?,?)", [
                                        id_usuario, cargo])

                            con.commit()
                            mensaje = " Usuario Administrador registrado con exito" 

            else:
                frm = Login()
                mensaje = "La página que desea acceder no esta disponible"
                return render_template("login.html", frm=frm,mensaje=mensaje)

    else:
        frm = Login()
        mensaje = "La página que desea acceder no esta disponible"
        return render_template("login.html", frm=frm,mensaje=mensaje)                
               

    return render_template("registroadmin.html", frm=frm, mensaje = mensaje)



# crear citas------------------------------------------------------------------------------------------------

@app.route('/crearcitas', methods=["Get","POST"])
def crear_citas():
    frm = Crearcitas()
    mensaje = ""
    rows = None

    if 'tipousuario' in session:
        if session["tipousuario"] == 'Medico' or session["tipousuario"] == 'Administrador' :
           
            if frm.validate_on_submit():
                if frm.crear:
                    fecha = frm.fecha.data
                    direccion = frm.direccion.data
                    
                    # Conecta a la BD
                    with sqlite3.connect("clinica.db") as con:
                        # Crea un cursor para manipular la BD
                        
                        cur = con.cursor()
                        # Prepara la sentencia SQL
                        cur.execute("INSERT INTO citamedica ( id_medico, fecha, direccion, estado) VALUES (?,?,?,'Sin asignar')", [
                                session["id_usuario"],  fecha, direccion])
                        # Ejecuta la sentencia SQL
                        con.commit()
                        mensaje = "Cita Creada con éxito"

            with sqlite3.connect("clinica.db") as con:# buscar en la tabla citamedica para mostrar en el html
                # Crea un cursor para manipular la BD
                con.row_factory = sqlite3.Row  # Lista de diccionario
                cur = con.cursor()
                cur.execute("SELECT id_cita, fecha, direccion FROM citamedica WHERE estado = 'Sin asignar' AND id_medico = ?", [
                                session["id_usuario"]])
                rows = cur.fetchall() 

        else:
            frm = Login()
            mensaje = "La página que desea acceder no esta disponible"
            return render_template("login.html", frm=frm,mensaje=mensaje)

    else:
        frm = Login()
        mensaje = "La página que desea acceder no esta disponible"
        return render_template("login.html", frm=frm,mensaje=mensaje)


    return render_template ("crearcitas.html", frm=frm, rows=rows, mensaje=mensaje)


#eliminar cita------------------------------------------
@app.route('/eliminarcita/<idcita>', methods=["GET"])
def eliminar_cita(idcita):
    frm = Crearcitas()
    mensaje = ""
    rows = []
    try:

        # Conecta a la BD
            with sqlite3.connect("clinica.db") as con:
                # Crea un cursor para manipular la BD
                idcita = int(idcita)
                cur = con.cursor()
                # Prepara la sentencia SQL
                cur.execute("DELETE FROM citamedica WHERE id_cita = ?", [idcita])
                # Ejecuta la sentencia SQL
                con.commit()
                mensaje = "Cita eliminada con éxito"
                       

            with sqlite3.connect("clinica.db") as con:
                # Crea un cursor para manipular la BD
                con.row_factory = sqlite3.Row  # Lista de diccionario
                cur = con.cursor()
                cur.execute("SELECT id_cita, fecha, direccion FROM citamedica WHERE estado = 'Sin asignar' AND  id_medico = ?", [session["id_usuario"]])
                rows = cur.fetchall()    

    except:

            mensaje = "No se pudo eliminar la cita"
            
   

    return render_template ("crearcitas.html", frm=frm, rows=rows, mensaje=mensaje)




#Pacientes Asignados--------------------------

@app.route('/pacientes_asignados', methods=["Get"])
def pacientes_asignados():
    if 'tipousuario' in session:
            if session["tipousuario"] == 'Medico' or session["tipousuario"] == 'Administrador' :


                with sqlite3.connect("clinica.db") as con:
                    # Crea un cursor para manipular la BD
                    con.row_factory = sqlite3.Row  # Lista de diccionario
                    cur = con.cursor()
                    cur.execute("SELECT c.id_cita, u.nombre, c.fecha, c.id_paciente FROM citamedica c  INNER  JOIN usuario u on c.id_paciente = u.id_usuario WHERE c.id_medico = ? AND c.estado = 'Asignada'", [session["id_usuario"]])
                    rows = cur.fetchall()    

            else:
                frm = Login()
                mensaje = "La página que desea acceder no esta disponible"
                return render_template("login.html", frm=frm,mensaje=mensaje)

    else:
        frm = Login()
        mensaje = "La página que desea acceder no esta disponible"
        return render_template("login.html", frm=frm,mensaje=mensaje)        


    return render_template("/pacientes_asignados.html", rows=rows)     



# Historial clinico medico---------------corregir------------------carga historia clinica de todos los pasientes ------------------------------     

@app.route('/historial_clinico_medico/<id_paciente>', methods=["Get"])
def historial_clinico_medico(id_paciente):

    if 'tipousuario' in session:
            if session["tipousuario"] == 'Medico' or session["tipousuario"] == 'Administrador' :


                with sqlite3.connect("clinica.db") as con:
                    # Crea un cursor para manipular la BD
                    con.row_factory = sqlite3.Row  # Lista de diccionario
                    cur = con.cursor()
                    cur.execute("SELECT c.id_cita, u.nombre, c.motivoconsulta, c.diagnostico, c.comentariomedico, c.fecha, c.id_paciente, m.nombre AS med FROM citamedica c  INNER  JOIN usuario u on c.id_paciente = u.id_usuario INNER  JOIN usuario m on c.id_medico = m.id_usuario WHERE  c.estado = 'Atendido' AND  c.id_paciente = ? ", [id_paciente] )
                        
                    rows = cur.fetchall()    

            else:
                frm = Login()
                mensaje = "La página que desea acceder no esta disponible"
                return render_template("login.html", frm=frm,mensaje=mensaje)

    else:
        frm = Login()
        mensaje = "La página que desea acceder no esta disponible"
        return render_template("login.html", frm=frm,mensaje=mensaje)

    return render_template("/historial_clinico_medico.html", rows=rows)


# Pacientes Atendidos---------------------------------------------------------------     

@app.route('/pacientes_atendidos', methods=["Get"])
def pacientes_atendidos():

    if 'tipousuario' in session:
            if session["tipousuario"] == 'Medico' or session["tipousuario"] == 'Administrador' :


                with sqlite3.connect("clinica.db") as con:
                    # Crea un cursor para manipular la BD
                    con.row_factory = sqlite3.Row  # Lista de diccionario
                    cur = con.cursor()
                    cur.execute("SELECT c.id_cita, c.fecha, u.nombre , c.motivoconsulta, c.diagnostico, c.comentariomedico,  c.id_paciente  FROM citamedica c  INNER  JOIN usuario u on c.id_paciente = u.id_usuario  WHERE   c.estado = 'Atendido' AND c.id_medico = ?", [session["id_usuario"]])
                    rows = cur.fetchall()    
            else:
                frm = Login()
                mensaje = "La página que desea acceder no esta disponible"
                return render_template("login.html", frm=frm,mensaje=mensaje)

    else:
        frm = Login()
        mensaje = "La página que desea acceder no esta disponible"
        return render_template("login.html", frm=frm,mensaje=mensaje)



    return render_template("/pacientes_atendidos.html",rows=rows)






# Historia clinica paciente----------------------------------------------------------------

@app.route('/historia_clinica_paciente/<id_paciente>', methods=["Get"])
def historia_clinica_paciente(id_paciente):

    if 'tipousuario' in session:
            if session["tipousuario"] == 'Paciente' or session["tipousuario"] == 'Administrador' :


                with sqlite3.connect("clinica.db") as con:
                    # Crea un cursor para manipular la BD
                    con.row_factory = sqlite3.Row  # Lista de diccionario
                    cur = con.cursor()
                    cur.execute("SELECT c.id_cita, c.motivoconsulta, c.diagnostico, c.comentariomedico, c.fecha, c.peso, c.estatura, u.nombre, c.calificacion  FROM citamedica c  INNER  JOIN usuario u on c.id_medico = u.id_usuario WHERE  c.estado = 'Atendido' AND  c.id_paciente = ? ", [session['id_usuario']])
                    rows = cur.fetchall()    

            else:
                frm = Login()
                mensaje = "La página que desea acceder no esta disponible"
                return render_template("login.html", frm=frm,mensaje=mensaje)

    else:
        frm = Login()
        mensaje = "La página que desea acceder no esta disponible"
        return render_template("login.html", frm=frm,mensaje=mensaje)

    
    return render_template("/historia_clinica_paciente.html", rows=rows)


# Calificar Atencion-------------------------------------------------

@app.route('/calificaratencion/<idcita>', methods=["Get","POST"])
def calificar_atencion(idcita):
    frm = Calificar()
    mensaje = ""
    if 'tipousuario' in session:
        if session["tipousuario"] == 'Paciente' or session["tipousuario"] == 'Administrador' :



            if frm.validate_on_submit():
                if frm.calificar:
                    calificacion = frm.calificacion.data  
                    
                    # Conecta a la BD
                    with sqlite3.connect("clinica.db") as con:
                        # Crea un cursor para manipular la BD
                        cur = con.cursor()
                        # Prepara la sentencia SQL
                        cur.execute("UPDATE citamedica SET calificacion = ?  WHERE id_cita = ?",[calificacion, idcita])

                        # Ejecuta la sentencia SQL
                        con.commit()
                        mensaje ="Calificada con exito"

        else:
            frm = Login()
            mensaje = "La página que desea acceder no esta disponible"
            return render_template("login.html", frm=frm,mensaje=mensaje)

    else:
        frm = Login()
        mensaje = "La página que desea acceder no esta disponible"
        return render_template("login.html", frm=frm,mensaje=mensaje)                


    return render_template("/calificaratencion.html", frm=frm, mensaje = mensaje )  


# conozcanos----------------------

@app.route('/conozcanos', methods=["Get"])
def conozcanos():
      return render_template("/conozcanos.html")

# contactenos------------------------------------------------------------------

@app.route('/contactenos', methods=["Get"])
def contactenos():
    return render_template("/contactenos.html")



#Nueva Consulta ------------------------------------------------------------------------------------

@app.route('/nuevaconsulta/<idcita>', methods=["Get","POST"])
def nuevaconsulta(idcita):
    frm = Nuevaconsulta()
    mensaje = ""

    if 'tipousuario' in session:
        if session["tipousuario"] == 'Medico' or session["tipousuario"] == 'Administrador' :
     
            if frm.validate_on_submit():
                if frm.guardar:
                    hora = frm.hora.data
                    peso = frm.peso.data
                    estatura = frm.estatura.data
                    ocupacion = frm.ocupacion.data
                    motivoconsulta = frm.motivoconsulta.data
                    diagnostico = frm.diagnostico.data
                    comentariomedico = frm.comentariomedico.data
                            
                    # Conecta a la BD
                    with sqlite3.connect("clinica.db") as con:
                        # Crea un cursor para manipular la BD
                        cur = con.cursor()
                        # Prepara la sentencia SQL
                        cur.execute("UPDATE citamedica SET hora = ?, peso = ?, estatura = ?, ocupacion = ?, motivoconsulta = ?, diagnostico = ?, comentariomedico = ? , estado = 'Atendido', calificacion = 0 WHERE id_cita = ?", [hora, peso, estatura, ocupacion, motivoconsulta, diagnostico, comentariomedico,idcita])
                        # Ejecuta la sentencia SQL
                        con.commit()
                        mensaje ="Guardado con exito"
                frm.id_cita.value = idcita    
        else:
            frm = Login()
            mensaje = "La página que desea acceder no esta disponible"
            return render_template("login.html", frm=frm,mensaje=mensaje)

    else:
        frm = Login()
        mensaje = "La página que desea acceder no esta disponible"
        return render_template("login.html", frm=frm,mensaje=mensaje)        

    return render_template("/nuevaconsulta.html", frm=frm, mensaje = mensaje)   


# solicitar cita medica-------------------------

@app.route('/solicitar_cita_medica', methods=["Get","POST"])#probaaaaaaaaaarrrrrrrrr
def solicitar_cita_medica():
  
    frm = Solicitarcita()
    nombre = frm.nombre.data
    mensaje = ""
    rows = None

    if 'tipousuario' in session:
        if session["tipousuario"] == 'Paciente' or session["tipousuario"] == 'Administrador' :

            if str(nombre) == 'None':
                nombre = ''

            Sentencia = "SELECT c.id_cita, c.fecha, c.direccion , u.nombre, m.especialidad FROM citamedica c      INNER JOIN medico m ON c.id_medico = m.id_medico INNER JOIN usuario u ON m.id_medico = u.id_usuario WHERE c.estado = 'Sin asignar' AND nombre LIKE '%" + str(nombre) + "%' "

            if frm.validate_on_submit():
                if frm.buscar:
                    
                    fecha = frm.fecha.data
                    especialidad = frm.especialidad.data

                    if especialidad != '0':
                        Sentencia = Sentencia + " AND especialidad = '" + str(especialidad) + "'" 
                
                    if fecha != '':
                        Sentencia = Sentencia + " AND fecha = '" + str(fecha) + "'" 
                

            with sqlite3.connect("clinica.db") as con:
                        # Crea un cursor para manipular la BD
                        con.row_factory = sqlite3.Row  # Lista de diccionario
                        cur = con.cursor()
                        cur.execute(Sentencia)
                        rows = cur.fetchall()   
        else:
            frm = Login()
            mensaje = "La página que desea acceder no esta disponible"
            return render_template("login.html", frm=frm,mensaje=mensaje)

    else:
        frm = Login()
        mensaje = "La página que desea acceder no esta disponible"
        return render_template("login.html", frm=frm,mensaje=mensaje)                

    return render_template ("solicitar_cita_medica.html", frm=frm, rows = rows, mensaje = mensaje)


    #-----------------------------------------------------------------

@app.route('/asignarcita/<idcita>', methods=["Get"])
def asignar_cita_medica(idcita):
  
    frm = Solicitarcita()
    nombre = frm.nombre.data
    mensaje = ""

    if str(nombre) == 'None':
        nombre = ''

    rows = []
   

        # Conecta a la BD
    with sqlite3.connect("clinica.db") as con:
        # Crea un cursor para manipular la BD
        idcita = int(idcita)
        cur = con.cursor()
        # Prepara la sentencia SQL
        cur.execute("UPDATE citamedica SET id_paciente = ?, estado = 'Asignada' WHERE id_cita = ? ", [session["id_usuario"], idcita])
        # Ejecuta la sentencia SQL
        con.commit()
        mensaje = "Cita asignada con éxito"
                      
           
    

           # mensaje = "No se pudo asignar la cita"

    Sentencia = "SELECT c.id_cita, c.fecha, c.direccion , u.nombre, m.especialidad FROM citamedica c      INNER JOIN medico m ON c.id_medico = m.id_medico INNER JOIN usuario u ON m.id_medico = u.id_usuario WHERE c.estado = 'Sin asignar' AND nombre LIKE '%" + str(nombre) + "%' "
   
           

    with sqlite3.connect("clinica.db") as con:
                # Crea un cursor para manipular la BD
                con.row_factory = sqlite3.Row  # Lista de diccionario
                cur = con.cursor()
                cur.execute(Sentencia)
                rows = cur.fetchall()   

    return render_template ("solicitar_cita_medica.html", frm=frm, rows = rows, mensaje = mensaje)


#Editar comentario--------------------------

@app.route('/editarcomentario/<id_cita>', methods=["Get","POST"])
def editarcomentario(id_cita):

    frm = Editarcomentario()
    mensaje = ""
    if 'tipousuario' in session:
            if session["tipousuario"] == 'Medico' or session["tipousuario"] == 'Administrador' :


                
                if frm.validate_on_submit():
                    if frm.guardar:
                        comentariomedico = frm.comentariomedico.data
                                
                        # Conecta a la BD
                        with sqlite3.connect("clinica.db") as con:
                            # Crea un cursor para manipular la BD
                            cur = con.cursor()
                            # Prepara la sentencia SQL
                            cur.execute("UPDATE citamedica SET  comentariomedico = ? , estado = 'Atendido' WHERE id_cita = ?", [comentariomedico,id_cita])
                            # Ejecuta la sentencia SQL
                            con.commit()
                            mensaje ="Comentario Editado con exito"

            else:
                frm = Login()
                mensaje = "La página que desea acceder no esta disponible"
                return render_template("login.html", frm=frm,mensaje=mensaje)

    else:
        frm = Login()
        mensaje = "La página que desea acceder no esta disponible"
        return render_template("login.html", frm=frm,mensaje=mensaje)                
        


    return render_template("/editarcomentario.html", frm=frm, mensaje=mensaje)  


#perfil usuario paciente-------- 

@app.route('/perfil_usuario_paciente', methods=["Get"])
def usuario_paciente():

    if 'tipousuario' in session:
        if session["tipousuario"] == 'Paciente' or session["tipousuario"] == 'Administrador' :

            with sqlite3.connect("clinica.db") as con:
                # Crea un cursor para manipular la BD
                con.row_factory = sqlite3.Row  # Lista de diccionario
                cur = con.cursor()
                cur.execute("SELECT u.nombre, u.numerodocumento, u.correo, u.genero, u.direccion, u.telefono, p.eps   FROM usuario u INNER JOIN paciente p ON p.id_paciente = u.id_usuario WHERE  id_usuario = ?", [session['id_usuario']])
                rows = cur.fetchall()     

    
        else:
            frm = Login()
            mensaje = "La página que desea acceder no esta disponible"
            return render_template("login.html", frm=frm,mensaje=mensaje)

    else:
        frm = Login()
        mensaje = "La página que desea acceder no esta disponible"
        return render_template("login.html", frm=frm,mensaje=mensaje)

    
    return render_template ("perfil_usuario_paciente.html", rows=rows )



#Perfil del medico--------------------------

@app.route('/perfil_usuario_medico', methods=["Get"])
def perfil_usuario_medico():

    if 'tipousuario' in session:
        if session["tipousuario"] == 'Medico' or session["tipousuario"] == 'Administrador' :


            with sqlite3.connect("clinica.db") as con:
                # Crea un cursor para manipular la BD
                con.row_factory = sqlite3.Row  # Lista de diccionario
                cur = con.cursor()
                cur.execute("SELECT  u.nombre, u.numerodocumento, u.correo, u.genero, u.direccion, u.telefono, m.especialidad   FROM usuario u INNER JOIN medico m ON m.id_medico = u.id_usuario WHERE  id_usuario = ?", [session['id_usuario']])
                rows = cur.fetchall()  

        else:
            frm = Login()
            mensaje = "La página que desea acceder no esta disponible"
            return render_template("login.html", frm=frm,mensaje=mensaje)

    else:
        frm = Login()
        mensaje = "La página que desea acceder no esta disponible"
        return render_template("login.html", frm=frm,mensaje=mensaje)        

    
    return render_template("/perfil_usuario_medico.html", rows = rows )  


# Mapa de Navegacion--------------------------

@app.route('/mapadenavegacion', methods=["Get"])
def mapadenavegacion():
     return render_template("/mapadenavegacion.html")  

# Atualizar Datos Paciente--------------------------

@app.route('/actualizardatospaciente', methods=["Get","POST"])
def actualizardatospaciente():
    frm= Actualizardatospaciente()
    mensaje = ""
    if 'tipousuario' in session:
        if session["tipousuario"] == 'Paciente' or session["tipousuario"] == 'Administrador' :
    
            if frm.validate_on_submit():
                if frm.enviar:
                    tipodocumento = frm.tipodocumento.data
                    numerodocumento = frm.numerodocumento.data
                    nombre = frm.nombre.data
                    correo = frm.correo.data
                    fechanacimiento = frm.fechanacimiento.data
                    genero = frm.genero.data
                    direccion = frm.direccion.data
                    telefono = frm.telefono.data
                    contrasena = frm.contrasena.data
                    eps = frm.eps.data
                    # Cifra la contraseña
                    encrp = hashlib.sha256(contrasena.encode('utf-8'))
                    pass_enc = encrp.hexdigest()

                    # Conecta a la BD
                    with sqlite3.connect("clinica.db") as con:
                        # Crea un cursor para manipular la BD
                        cur = con.cursor()
                        #cur.execute("SELECT  u. tipodocumento, u.numerodocumento, u.nombre, u.correo, u.fechanacimiento, u.genero, u.direccion, u.telefono, u.pass_enc, p.eps  FROM usuario u INNER JOIN paciente p ON p.id_paciente = u.id_usuario WHERE  id_usuario = ?", [session['id_usuario']])
                        

                        # Prepara la sentencia SQL
                        cur.execute("UPDATE usuario SET tipodocumento = ?, numerodocumento = ?, nombre = ?, correo = ?, fechanacimiento = ?, genero = ?, direccion = ?, telefono = ?, contrasena = ? WHERE id_usuario = ?", [tipodocumento, numerodocumento, nombre, correo, fechanacimiento, genero, direccion, telefono, pass_enc, session['id_usuario']])

                        cur.execute("UPDATE paciente SET eps = ? WHERE id_paciente = ?", [eps, session['id_usuario']])

                        # Ejecuta la sentencia SQL
                        con.commit()
                        mensaje ="Actualizado con exito"

        else:
            frm = Login()
            mensaje = "La página que desea acceder no esta disponible"
            return render_template("login.html", frm=frm,mensaje=mensaje)

    else:
        frm = Login()
        mensaje = "La página que desea acceder no esta disponible"
        return render_template("login.html", frm=frm,mensaje=mensaje)

    return render_template("/actualizardatospaciente.html", frm = frm, mensaje = mensaje)      



#-----------Actualizar datos medico-----------------------------------------------------------------------


@app.route('/actualizardatosmedico', methods=["Get","POST"])
def actualizardatosmedico():
    
    frm= Actualizardatosmedico()
    mensaje = ""


    if 'tipousuario' in session:
            if session["tipousuario"] == 'Medico' or session["tipousuario"] == 'Administrador' :
                if frm.validate_on_submit():
                    if frm.enviar:
                        tipodocumento = frm.tipodocumento.data
                        numerodocumento = frm.numerodocumento.data
                        nombre = frm.nombre.data
                        correo = frm.correo.data
                        fechanacimiento = frm.fechanacimiento.data
                        genero = frm.genero.data
                        direccion = frm.direccion.data
                        telefono = frm.telefono.data
                        contrasena = frm.contrasena.data
                        especialidad = frm.especialidad.data
                        # Cifra la contraseña
                        encrp = hashlib.sha256(contrasena.encode('utf-8'))
                        pass_enc = encrp.hexdigest()

                        # Conecta a la BD
                        with sqlite3.connect("clinica.db") as con:
                            # Crea un cursor para manipular la BD
                            cur = con.cursor()
                            
                            

                            # Prepara la sentencia SQL
                            cur.execute("UPDATE usuario SET tipodocumento = ?, numerodocumento = ?, nombre = ?, correo = ?, fechanacimiento = ?, genero = ?, direccion = ?, telefono = ?, contrasena = ? WHERE id_usuario = ?", [tipodocumento, numerodocumento, nombre, correo, fechanacimiento, genero, direccion, telefono, pass_enc, session['id_usuario']])

                            cur.execute("UPDATE medico SET especialidad = ? WHERE id_medico = ?", [especialidad, session['id_usuario']])

                            # Ejecuta la sentencia SQL
                            con.commit()
                            mensaje ="Actualizado con Exito"
            else:
                frm = Login()
                mensaje = "La página que desea acceder no esta disponible"
                return render_template("login.html", frm=frm,mensaje=mensaje)

    else:
        frm = Login()
        mensaje = "La página que desea acceder no esta disponible"
        return render_template("login.html", frm=frm,mensaje=mensaje)            
    
    return render_template("/actualizardatosmedico.html", frm = frm, mensaje = mensaje) 



#consultar y cancelar cita--------------------------

@app.route('/consultarcancelarcitas', methods=["Get"])
def gconsultarcancelarcitas():

    if 'tipousuario' in session:
            if session["tipousuario"] == 'Paciente' or session["tipousuario"] == 'Administrador' :


                with sqlite3.connect("clinica.db") as con:
                    # Crea un cursor para manipular la BD
                    con.row_factory = sqlite3.Row  # Lista de diccionario
                    cur = con.cursor()

                    cur.execute("SELECT c.id_cita, u.nombre, c.direccion, c.fecha, c.id_medico FROM citamedica c  INNER  JOIN usuario u on c.id_medico = u.id_usuario WHERE c.id_paciente = ? AND c.estado = 'Asignada'", [session["id_usuario"]])
                    rows = cur.fetchall()    

            else:
                frm = Login()
                mensaje = "La página que desea acceder no esta disponible"
                return render_template("login.html", frm=frm,mensaje=mensaje)

    else:
        frm = Login()
        mensaje = "La página que desea acceder no esta disponible"
        return render_template("login.html", frm=frm,mensaje=mensaje)        
        
    return render_template("/consultarcancelarcitas.html",rows = rows )  




#cancelar cita------------------------------------------


@app.route('/cancelarcita/<idcita>', methods=["GET"])
def cancelar_cita(idcita):


            
     with sqlite3.connect("clinica.db") as con:
                # Crea un cursor para manipular la BD
                cur = con.cursor()
                # Prepara la sentencia SQL
                cur.execute("UPDATE citamedica SET  estado = 'Sin asignar', id_paciente = null   WHERE id_cita = ?",
                [ idcita])

                # Ejecuta la sentencia SQL
                con.commit()
                rows = cur.fetchall()

      
     with sqlite3.connect("clinica.db") as con:
        # Crea un cursor para manipular la BD
        con.row_factory = sqlite3.Row  # Lista de diccionario
        cur = con.cursor()

        cur.execute("SELECT c.id_cita, u.nombre, c.direccion, c.fecha, c.id_medico FROM citamedica c  INNER  JOIN usuario u on c.id_medico = u.id_usuario WHERE c.id_paciente = ? AND c.estado = 'Asignada'", [session["id_usuario"]])
        rows = cur.fetchall()   

        
            
   

     return render_template ("consultarcancelarcitas.html", rows = rows)



# Perfil administrador------------------------------

@app.route("/perfil_admin")
def perfil_admin():

    if 'tipousuario' in session:
        if  session["tipousuario"] == 'Administrador' :

            with sqlite3.connect("clinica.db") as con:
                #Crea un cursor para manipular la BD
                con.row_factory = sqlite3.Row  # Lista de diccionario
                cur = con.cursor()
                cur.execute("SELECT* FROM usuario ")
                rows = cur.fetchall()     



            with sqlite3.connect("clinica.db") as con:
                # Crea un cursor para manipular la BD
                con.row_factory = sqlite3.Row  # Lista de diccionario
                cur = con.cursor()
                cur.execute("SELECT COUNT (*)  FROM usuario")
                rows2 = cur.fetchall()   


            with sqlite3.connect("clinica.db") as con:
                # Crea un cursor para manipular la BD
                con.row_factory = sqlite3.Row  # Lista de diccionario
                cur = con.cursor()
                cur.execute("SELECT COUNT (*)  FROM usuario WHERE tipousuario = 'Paciente'")
                rows3 = cur.fetchall()     


            with sqlite3.connect("clinica.db") as con:
                # Crea un cursor para manipular la BD
                con.row_factory = sqlite3.Row  # Lista de diccionario
                cur = con.cursor()
                cur.execute("SELECT COUNT (*)  FROM usuario WHERE tipousuario = 'Medico'")
                rows4 = cur.fetchall()      


            with sqlite3.connect("clinica.db") as con:
                # Crea un cursor para manipular la BD
                con.row_factory = sqlite3.Row  # Lista de diccionario
                cur = con.cursor()
                cur.execute("SELECT COUNT (*)  FROM citamedica")
                rows5 = cur.fetchall()   


            with sqlite3.connect("clinica.db") as con:
                # Crea un cursor para manipular la BD
                con.row_factory = sqlite3.Row  # Lista de diccionario
                cur = con.cursor()
                cur.execute("SELECT COUNT (*)  FROM citamedica WHERE estado = 'Asignada'")
                rows6 = cur.fetchall()             


            with sqlite3.connect("clinica.db") as con:
                # Crea un cursor para manipular la BD
                con.row_factory = sqlite3.Row  # Lista de diccionario
                cur = con.cursor()
                cur.execute("SELECT COUNT (*)  FROM citamedica WHERE estado = 'Sin asignar'")
                rows7 = cur.fetchall()  


            with sqlite3.connect("clinica.db") as con:
                # Crea un cursor para manipular la BD
                con.row_factory = sqlite3.Row  # Lista de diccionario
                cur = con.cursor()
                cur.execute("SELECT COUNT (*)  FROM citamedica WHERE estado = 'Atendido'")
                rows8 = cur.fetchall()     


            with sqlite3.connect("clinica.db") as con:
                # Crea un cursor para manipular la BD
                con.row_factory = sqlite3.Row  # Lista de diccionario
                cur = con.cursor()
                cur.execute("SELECT COUNT (*)  FROM usuario WHERE tipousuario = 'Administrador'")
                rows9 = cur.fetchall()         
        else:
            frm = Login()
            mensaje = "La página que desea acceder no esta disponible"
            return render_template("login.html", frm=frm,mensaje=mensaje)

    else:
        frm = Login()
        mensaje = "La página que desea acceder no esta disponible"
        return render_template("login.html", frm=frm,mensaje=mensaje)


    return render_template("/perfil_admin.html", rows = rows, rows2 = rows2, rows3 = rows3, rows4 = rows4, rows5 = rows5, rows6 =rows6, rows7 = rows7,rows8 =rows8,  rows9 = rows9 )

# Perfil administrador gestionar usuarios----------------------------------


@app.route("/gestionar_usuarios_admin", methods=["GET", "POST"])
def gestionar_usuarios_admin():
    if 'tipousuario' in session:
            if session["tipousuario"] ==  'Administrador' :


                with sqlite3.connect("clinica.db") as con:
                    con.row_factory = sqlite3.Row
                    cur = con.cursor()
                    cur.execute("SELECT * FROM usuario ORDER BY tipousuario, numerodocumento ASC")
                    rows = cur.fetchall()        

            else:
                frm = Login()
                mensaje = "La página que desea acceder no esta disponible"
                return render_template("login.html", frm=frm,mensaje=mensaje)

    else:
        frm = Login()
        mensaje = "La página que desea acceder no esta disponible"
        return render_template("login.html", frm=frm,mensaje=mensaje)




    return render_template("/gestionar_usuarios_admin.html", rows=rows)



#-----------------------------------------------------------------------------------------------------------


@app.route("/gestionar_usuarios_admin_borrar/<id_usuario>", methods=["GET", "POST"])
def gestionar_usuarios_admin_borrar(id_usuario):    

    if 'tipousuario' in session:
            if session["tipousuario"] ==  'Administrador' :
                with sqlite3.connect("clinica.db") as con:
                        con.row_factory = sqlite3.Row
                        cur = con.cursor()
                        cur.execute("SELECT * FROM usuario WHERE id_usuario = ?", [id_usuario])
                        rows = cur.fetchall()
            else:
                frm = Login()
                mensaje = "La página que desea acceder no esta disponible"
                return render_template("login.html", frm=frm,mensaje=mensaje)

    else:
        frm = Login()
        mensaje = "La página que desea acceder no esta disponible"
        return render_template("login.html", frm=frm,mensaje=mensaje)

    return render_template("/gestionar_usuarios_admin_borrar.html", rows=rows)


#------------------------------------------------------------------------------------------------------    

@app.route('/eliminarusuario/<id_usuario>', methods=["GET"])
def eliminar_usuario(id_usuario):
    mensaje = ""   

    if 'tipousuario' in session:
            if session["tipousuario"] ==  'Administrador' :
                try:
                    with sqlite3.connect("clinica.db") as con:
                        id_usuario = int(id_usuario)
                        cur = con.cursor()
                        cur.execute("DELETE FROM usuario WHERE id_usuario = ?", [id_usuario])
                        con.commit()
                        mensaje = "Usuario eliminado con éxito"

                        with sqlite3.connect("clinica.db") as con:
                            con.row_factory = sqlite3.Row
                            cur = con.cursor()
                            cur.execute("SELECT * FROM usuario ORDER BY tipousuario, numerodocumento ASC")
                            rows = cur.fetchall()
                except:
                        mensaje = "No se pudo eliminar el usuario"
            else:
                    frm = Login()
                    mensaje = "La página que desea acceder no esta disponible"
                    return render_template("login.html", frm=frm,mensaje=mensaje)

    else:
        frm = Login()
        mensaje = "La página que desea acceder no esta disponible"
        return render_template("login.html", frm=frm,mensaje=mensaje)



    return render_template ("/gestionar_usuarios_admin.html", mensaje=mensaje, rows=rows)




# Perfil administrador gestionar citas-----------------------------------------

@app.route("/gestionar_citas_admin")
def gestionar_citas_admin():
    if 'tipousuario' in session:
            if session["tipousuario"] ==  'Administrador' :


                with sqlite3.connect("clinica.db") as con:
                    con.row_factory = sqlite3.Row
                    cur = con.cursor()
                    cur.execute("SELECT c.fecha, c.hora, c.estado, c.calificacion, p.numerodocumento, c.id_paciente, p.nombre AS pacien, c.id_medico, m.nombre AS medi FROM citamedica c INNER JOIN usuario p on c.id_paciente = p.id_usuario INNER JOIN usuario m ON c.id_medico = m.id_usuario ORDER BY c.fecha, p.numerodocumento ASC")
                    rows = cur.fetchall()
            else:
                frm = Login()
                mensaje = "La página que desea acceder no esta disponible"
                return render_template("login.html", frm=frm,mensaje=mensaje)

    else:
        frm = Login()
        mensaje = "La página que desea acceder no esta disponible"
        return render_template("login.html", frm=frm,mensaje=mensaje)      


    return render_template("/gestionar_citas_admin.html", rows=rows)

# Perfil administrador gestionar historia clinica----------------------------------------

@app.route("/gestionar_historia_clinica_admin")
def gestionar_historia_clinica_admin():
    if 'tipousuario' in session:
            if session["tipousuario"] ==  'Administrador' :


                with sqlite3.connect("clinica.db") as con:
                    con.row_factory = sqlite3.Row
                    cur = con.cursor()
                    cur.execute("SELECT c.id_paciente, u.numerodocumento, u.nombre, MAX(c.fecha) AS ultimacita FROM citamedica c INNER JOIN usuario u on c.id_paciente = u.id_usuario GROUP BY u.numerodocumento ")
                    rows = cur.fetchall()

            else:
                    frm = Login()
                    mensaje = "La página que desea acceder no esta disponible"
                    return render_template("login.html", frm=frm,mensaje=mensaje)

    else:
        frm = Login()
        mensaje = "La página que desea acceder no esta disponible"
        return render_template("login.html", frm=frm,mensaje=mensaje)   


    return render_template("/gestionar_historia_clinica_admin.html", rows=rows)
  

@app.route('/historia_clinica_paciente_admin/<id_paciente>', methods=["Get"])
def historia_clinica_paciente_admin(id_paciente):
     with sqlite3.connect("clinica.db") as con:
        # Crea un cursor para manipular la BD
        con.row_factory = sqlite3.Row  # Lista de diccionario
        cur = con.cursor()
        cur.execute("SELECT c.id_cita, c.motivoconsulta, c.diagnostico, c.comentariomedico, c.fecha, c.peso, c.estatura, u.nombre  FROM citamedica c  INNER  JOIN usuario u on c.id_medico = u.id_usuario WHERE  c.estado = 'Atendido' AND  c.id_paciente = ? ", [id_paciente])
        rows = cur.fetchall()        
        return render_template("/historia_clinica_paciente.html", rows=rows)

if __name__ == '__main__':
    app.run(debug=True)