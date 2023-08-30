from flask_sqlalchemy import SQLAlchemy

#Inicializamos la extension SQLAlchemy

db = SQLAlchemy()

#Definimos una clase que representa una tabla en la base de datos
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False )
    apellido = db.Column(db.String(50), nullable=False )
    cedula = db.Column(db.Integer, nullable=False )
    mail = db.Column(db.String(50), nullable=False )
    numero = db.Column(db.Integer, nullable=False )
    direccion = db.Column(db.String(50), nullable=False )

    #Constructor de clase
    def __init__(self, nombre, apellido, cedula,mail,numero,direccion):
        self.nombre = nombre
        self.apellido = apellido
        self.cedula=cedula
        self.mail=mail
        self.numero=numero
        self.direccion=direccion
        
class Contactos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.Integer, nullable=False)
    e_mail = db.Column(db.String(200), nullable=False)

    def __init__(self, nombre, apellido, telefono, e_mail):
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.e_mail = e_mail