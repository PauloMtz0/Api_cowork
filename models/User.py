from config import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    app = db.Column(db.String(100), nullable=False)
    apm = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(150), unique=True, nullable=False)
    sexo = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    huella = db.Column(db.Text, nullable=False)
    fecha_registro = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    passw = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(100), nullable=False)
    
    def __init__(self, nombre, app, apm, correo, sexo, fecha_nacimiento, huella, passw, rol):
        self.nombre = nombre
        self.app = app
        self.apm = apm
        self.correo = correo
        self.sexo = sexo
        self.fecha_nacimiento = fecha_nacimiento
        self.huella = huella
        self.passw = generate_password_hash(passw)
        self.rol = rol



    def check_password (self, passw):
            return check_password_hash(self.passw, passw); 
    
   def to_dict(self):
    fecha_nacimiento = self.fecha_nacimiento
    if isinstance(fecha_nacimiento, str):
        fecha_str = fecha_nacimiento  # Ya es una cadena, no necesita conversión
    else:
        fecha_str = fecha_nacimiento.isoformat() if fecha_nacimiento else None

    fecha_registro = self.fecha_registro
    if isinstance(fecha_registro, str):
        registro_str = fecha_registro
    else:
        registro_str = fecha_registro.isoformat() if fecha_registro else None

    return {
        "id_usuario": self.id_usuario,
        "nombre": self.nombre,
        "app": self.app,
        "apm": self.apm,
        "correo": self.correo,
        "sexo": self.sexo,
        "fecha_nacimiento": fecha_str,
        "huella": self.huella,
        "fecha_registro": registro_str,
        "passw": self.passw,
        "rol": self.rol,
    }
    
