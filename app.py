#Importamos las librerias 
from flask import render_template, request, redirect,url_for
from conexion import app, db
from models import Usuario
from models import Contactos
import requests
import json
from twilio.rest import Client

TWILIO_ACCOUNT_SID = "ACf2fec9795a6edadb61dbf1b3665a70ab"  # ID de cuenta de Twilio
TWILIO_AUTH_TOKEN = "d9f68d5f3816005dbb9a8f61d16b0357"  # Token de autenticación de Twilio
TWILIO_PHONE_NUMBER = "+18145930672"  # Número de teléfono de Twilio
RECIPIENT_PHONE_NUMBER = "+595971895374"  # Número del destinatario

def get_location():
    ip = requests.get("https://api.ipify.org").text
    location_url = f"https://ipinfo.io//json{ip}/json"
    location_response = requests.get(location_url)
    location_data = json.loads(location_response.text)

    if "loc" in location_data:
        latitude, longitude = location_data["loc"].split(",")
        return latitude, longitude
    else:
        return None, None

#creamos la ruta principal de nuestra pagina

@app.route('/')
def index():
    return render_template('index.html')

#CRUD - CREAT / CARGAR - READ / MOSTRAR - UPDATE / ACTUALIZAR - DELETE / ELIMINAR

@app.route("/login",methods=["GET","POST"])
def login():
     return render_template("login.html")

@app.route('/registro_usuario', methods = ['GET','POST'])
def registro_usuario():
    #Si el metodo es POST obtenemos los datos 'nombre','apellido' y 'cedula'
    if request.method == 'POST':
        nombre = request.form['nombre']#Eduardo
        apellido = request.form['apellido']#Quinhonez
        cedula = request.form['cedula']
        mail=request.form["mail"]
        numero=request.form["numero"]
        direccion=request.form["direccion"]


        #Creamos un objeto de la clase Alumnos con los datos obtenidos
        datos_usuarios = Usuario(nombre, apellido, cedula,mail,numero,direccion)
        print(datos_usuarios)

        db.session.add(datos_usuarios)#Agregar a la sesion de la base de datos
        db.session.commit()#Confirmamos la carga de los datos

        return redirect(url_for("menu_usuario"))#Renderizamos la pagina HTML
    
    return render_template('registro_usuario.html')


@app.route('/mostrar_datos',methods = ['GET','POST'])
def mostrar_datos():

    lista_usuarios = Usuario.query.all()#Creamos el nuevo objeto que contiene la lista total de nuestra base de datos

    return render_template('mostrar_datos.html', lista_usuarios=lista_usuarios)

#Creamos la ruta actualizar donde solicitamos el ID del alumno para mostrar solo ese dato
@app.route('/actualizar/<int:usuario_id>', methods = ['GET', 'POST'])
def actualizar(usuario_id):#Pasamos la variable como parametro a nuestrsa funcion

    usuario_actualizado = Usuario.query.get(usuario_id)#Creamos un nuevo objeto donde obtenemos los datos de un alumno en especifico

    if request.method == 'POST':#Obtenemos los datos del formulario (nombre,apellido,cedula)
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        cedula = request.form['cedula']
        mail=request.form["mail"]
        numero=request.form["numero"]
        direccion=request.form["direccion"]


        #Actualizamos los datos obtenidos del formulario instanciando del nuevo objeto
        usuario_actualizado.nombre = nombre
        usuario_actualizado.apellido = apellido
        usuario_actualizado.cedula = cedula
        usuario_actualizado.mail= mail
        usuario_actualizado.numero=numero
        usuario_actualizado.direccion=direccion


        db.session.commit()#Confirmamos la actualizacion de los datos

        return redirect(url_for('mostrar_datos'))#Redireccionamos a la pagina una vez actualizado los datos.
    
    return render_template ('actualizar.html', usuario_actualizado=usuario_actualizado)

#Creamos la ruta para eliminar... esta ruta no tiene una pagina HTML ya que desde mostrar_datos.html podemos acceder a esta ruta de acuerdo a la configuracion que realizamos en la misma"
@app.route('/eliminar', methods= ['GET', 'POST'])
def eliminar():

    if request.method == 'POST':

        id = request.form['usuario_id'] #Guardamos en la variable id los datos obtenidos del formulario
        usuario_a_eliminar = Usuario.query.filter_by(id=id).first()#Realizamos la consulta a nuestra base de datos para obtener los datos del alumno en referencia y creamos un nuevo objeto guardando en la variable 

        db.session.delete(usuario_a_eliminar)#Eliminamos los datos del alumno
        db.session.commit()#Confirmamos la eliminacion 

        return redirect(url_for('mostrar_datos'))#Redireccionamos a la pagina para mostrar los datos de la base de datos

@app.route("/registro_contacto", methods=["GET", "POST"])
def registro_contacto():
        if request.method == "POST":
            nombre = request.form["nombre"]
            apellido = request.form["apellido"]
            telefono = request.form["telefono"]
            e_mail = request.form["e_mail"]

            datos_contactos = Contactos(nombre, apellido, e_mail, telefono)

            db.session.add(datos_contactos)

            db.session.commit()

            return redirect(url_for("listado_contactos"))#Renderizamos la pagina HTML
        return render_template('registro_contacto.html')



@app.route("/listado_contactos", methods=["GET", "POST"])
def listado_contactos():
        lista_contactos = Contactos.query.all()

        return render_template("listado_contactos.html", lista_contactos=lista_contactos)


@app.route("/actualizar_contactos/<int:contacto_id>", methods=["GET", "POST"])
def actualizar_contactos(contacto_id):
        contacto_actualizado = Contactos.query.get(contacto_id)

        if request.method == "POST":
            nombre = request.form["nombre"]
            apellido = request.form["apellido"]
            telefono = request.form["telefono"]
            e_mail = request.form["e_mail"]

            contacto_actualizado.nombre = nombre
            contacto_actualizado.apellido = apellido
            contacto_actualizado.telefono = telefono
            contacto_actualizado.e_mail = e_mail

            db.session.commit()

            return redirect(url_for("listado_contactos"))

        return render_template(
            "actualizar_contactos.html", contacto_actualizado=contacto_actualizado
        )


@app.route("/eliminar_contacto", methods=["GET", "POST"])
def eliminar_contacto():
        if request.method == "POST":
            id = request.form["contacto_id"]
            contacto_a_eliminar = Contactos.query.filter_by(id=id).first()
            db.session.delete(contacto_a_eliminar)
            db.session.commit()

            return redirect(url_for("listado_contactos"))

@app.route("/menu_usuario", methods=["GET", "POST"])
def menu_usuario():
    if request.method == "POST":
        latitude, longitude = get_location()

        if latitude is not None and longitude is not None:
            message = f"Mi ubicación actual es {latitude}, {longitude}"
            google_maps_link = f"https://www.google.com/maps/place/{latitude},{longitude}"
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            client.messages.create(
                body=f"¡Hola! {message}. Puedes ver mi ubicación en Google Maps: {google_maps_link}",
                from_=TWILIO_PHONE_NUMBER,
                to=RECIPIENT_PHONE_NUMBER
            )
            success_message = "Mensaje de texto enviado con éxito."
            print(success_message)
        else:
            success_message = "No se pudo obtener la ubicación."
            print(success_message)

        return render_template("menu_usuario.html", success_message=success_message)

    return render_template("menu_usuario.html")