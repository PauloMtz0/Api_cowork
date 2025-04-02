from flask import Blueprint, jsonify, request
from config import db
from controllers.ubicacionController import get_all_ubicaciones,create_ubicacion,update_ubicacion,delete_ubicacion,get_ubicacion

ubicacion_bp = Blueprint('ubicacion',__name__)
# Rutas de ubicaciones
@ubicacion_bp.route('/', methods=['GET'])
def get_ubicaciones():
    return jsonify(get_all_ubicaciones())

@ubicacion_bp.route('/<int:id>', methods=['GET'])
def get_single_ubicacion(id):
    ubicacion = get_ubicacion(id)
    return jsonify(ubicacion) if ubicacion else jsonify({'error': 'Ubicación no encontrada'}), 404

@ubicacion_bp.route('/', methods=['POST'])
def create_new_ubicacion():
    data = request.get_json()
    
    nombre = data.get('nombre')
    tipo = data.get('tipo')
    

    new_ubicacion = create_ubicacion(nombre, tipo)
    return jsonify(new_ubicacion), 201

# Actualizar ubicación
@ubicacion_bp.route('/<int:id>', methods=['PUT'])
def update_ubicacion_data(id):
    data = request.get_json()
    
    nombre = data.get('nombre')
    tipo = data.get('tipo')

    updated_ubicacion = update_ubicacion(id, nombre, tipo)
    
    if updated_ubicacion:
        return jsonify(updated_ubicacion)
    else:
        return jsonify({'error': 'Ubicación no encontrada'}), 404
    
# Eliminar ubicación    
@ubicacion_bp.route('/<int:id>', methods=['DELETE'])
def remove_ubicacion(id):
    return delete_ubicacion(id)

# Importar ubicaciones
@ubicacion_bp.route("/ubicaciones/importar", methods=["POST"])
def importar_ubicaciones():
    try:
        data = request.get_json()
        ubicaciones = data.get("ubicaciones", [])

        if not isinstance(ubicaciones, list) or not ubicaciones:
            return jsonify({"error": "El archivo no contiene datos válidos"}), 400

        valores = [(u["nombre"], u["tipo"]) for u in ubicaciones]

        sql = "INSERT INTO ubicacion (nombre, tipo) VALUES (%s, %s)"
        
        with db.cursor() as cursor:
            cursor.executemany(sql, valores)
            db.commit()
            return jsonify({"mensaje": "Ubicaciones importadas correctamente", "registros": cursor.rowcount})
    
    except Exception as e:
        return jsonify({"error": "Error al procesar la importación", "detalle": str(e)}), 500