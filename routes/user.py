from flask import Blueprint, jsonify, request
from controllers.userController import get_all_users, create_user, login_user, get_user, update_user, delete_user
from datetime import timedelta
from config import db



user_bp = Blueprint('usuarios',__name__)

def timedelta_to_str(td):
    if isinstance(td, timedelta):
        # Convertir a horas, minutos y segundos
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    return td

#Obtener todos los usuarios 
@user_bp.route('/', methods=['GET'])
def index():
    user = get_all_users()
    return jsonify(user)

# Obtener un usuario específico 
@user_bp.route('/<int:id_usuario>', methods=['GET'])
def get_one_user(id_usuario):
    user = get_user(id_usuario) 
    if user:
        return jsonify(user) 
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404  

# Crear un nuevo usuario
@user_bp.route('/', methods = ['POST'])
def user_store():
    data = request.get_json()
    nombre = data.get('nombre')
    app = data.get('app')
    apm = data.get('apm')
    correo = data.get('correo')
    sexo = data.get('sexo')
    fecha_nacimiento = data.get('fecha_nacimiento')
    huella = data.get('huella')
    passw = data.get('passw')
    rol = data.get('rol')
    
    print(f"Datos recibidos: {data}")
    print(f"NAME {nombre} --- email {correo}")
    new_user = create_user(nombre, app, apm, correo, sexo, fecha_nacimiento, huella, passw, rol)

    return jsonify(new_user)

# Eliminar un usuario
@user_bp.route('/<int:id_usuario>', methods=['DELETE'])
def user_destroy(id_usuario):
    user = delete_user(id_usuario)
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404
    

# Actualizar un usuario
@user_bp.route('/<int:id_usuario>', methods=['PUT'])
def user_update(id_usuario):
    data = request.get_json()
    nombre = data.get('nombre')
    app = data.get('app')
    apm = data.get('apm')
    correo = data.get('correo')
    sexo = data.get('sexo')
    fecha_nacimiento = data.get('fecha_nacimiento')
    huella = data.get('huella')
    passw = data.get('passw')
    rol = data.get('rol')

    user = update_user(id_usuario, nombre, app, apm, correo, sexo, fecha_nacimiento, huella, passw, rol)

    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404

#Login
@user_bp.route('/login',methods = ['POST'])
def login():
    data = request.get_json();
    return login_user(data['correo'], data['passw'])


# Importar usuarios
@user_bp.route("/usuarios/importar", methods=["POST"])
def importar_usuarios():
    try:
        data = request.get_json()
        usuarios = data.get("usuarios", [])

        if not isinstance(usuarios, list) or not usuarios:
            return jsonify({"error": "El archivo no contiene datos válidos"}), 400

        valores = [(u["nombre"], u["app"], u["apm"], u["correo"], u["sexo"], u["fecha_nacimiento"], u["rol"]) for u in usuarios]

        sql = "INSERT INTO usuarios (nombre, app, apm, correo, sexo, fecha_nacimiento, rol) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        
        with db.cursor() as cursor:
            cursor.executemany(sql, valores)
            db.commit()
            return jsonify({"mensaje": "Usuarios importados correctamente", "registros": cursor.rowcount})
    
    except Exception as e:
        return jsonify({"error": "Error al procesar la importación", "detalle": str(e)}), 500
    