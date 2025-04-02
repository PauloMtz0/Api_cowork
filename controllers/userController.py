from models.User import Usuarios
from flask import jsonify
from config import db
from flask_jwt_extended import create_access_token

def get_all_users():
    try: 
        return [  user.to_dict()  for user in Usuarios.query.all()]
    except Exception as error:
        print(f"error {error}")
        return jsonify({ 'msg' : 'error al crear usuario' }), 500

def create_user(nombre, app, apm, correo, sexo, fecha_nacimiento, huella, passw, rol):
    try:
        new_user = Usuarios(nombre, app, apm, correo, sexo, fecha_nacimiento, huella, passw, rol)

        db.session.add(new_user)
        db.session.commit()
        return new_user.to_dict()
    except Exception as e:
        print(f"ERROR {e}")
        

#actualizar usuario
def update_user(id_usuario, nombre, app, apm, correo, sexo, fecha_nacimiento, huella, passw, rol):
    try:
        user = Usuarios.query.get(id_usuario)
        if not user:
            return None

        user.nombre = nombre
        user.app = app
        user.apm = apm
        user.correo = correo
        user.sexo = sexo
        user.fecha_nacimiento = fecha_nacimiento
        user.huella = huella
        user.passw = passw
        user.rol = rol
        db.session.commit()

        return user.to_dict()
    except Exception as e:
        print(f"ERROR {e}")


#eliminar usuario
def delete_user(id_usuario):
    try:
        user = Usuarios.query.get(id_usuario)
        if not user:
            return {"error": "User not found"}  
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully"} 
    except Exception as e:
        db.session.rollback()
        print(f"ERROR {e}")
        return {"error": "An error occurred while deleting the user"}


# Obtener usuario específico
def get_user(id_usuario):
    try:
        user = Usuarios.query.get(id_usuario)
        return user.to_dict()
    except Exception as e:
        print(f"ERROR {e}")




def login_user (correo, passw):
        user = Usuarios.query.filter_by(correo=correo).first();

        if user and user.check_password(passw):
            access_token = create_access_token(identity=user.id_usuario);
            return jsonify({
                'access_token': access_token,
                'user': {
                    "id" : user.id_usuario,
                    "nombre" : user.nombre,
                    "correo" : user.correo
                }
            })
        return jsonify({"msg": "Credenciales invalidas"}), 401



#user = User.query.all();
#   print(user)