from flask import Blueprint, jsonify, request
from controllers.entradasSalidasController import get_all_entradas_salidas, create_entrada_salida, update_entrada_salida, delete_entrada_salida, get_entrada_salida


horario_bp = Blueprint('horarios',__name__)

@horario_bp.route('/', methods=['GET'])
def get_horarios():
    return jsonify(get_all_entradas_salidas())

@horario_bp.route('/<int:id>', methods=['GET'])
def get_single_horario(id):
    horario = get_entrada_salida(id)
    return jsonify(horario) if horario else jsonify({'error': 'Registro no encontrado'}), 404

@horario_bp.route('/', methods=['POST'])
def create_new_horario():
    data = request.get_json()
    id_usuario = data.get('id_usuario')
    id_ubicacion = data.get('id_ubicacion')
    hora_entrada = data.get('hora_entrada')
    hora_salida = data.get('hora_salida')

    new_horario = create_entrada_salida(id_usuario, id_ubicacion, hora_entrada, hora_salida)
    return jsonify(new_horario), 201

@horario_bp.route('/<int:id_horarios>', methods=['PUT'])
def update_horario_data(id_horarios):
    data = request.get_json()
    id_usuario = data.get('id_usuario')
    id_ubicacion = data.get('id_ubicacion')
    hora_entrada = data.get('hora_entrada')
    hora_salida = data.get('hora_salida')
    updated_horario = update_entrada_salida(id_horarios, id_usuario, id_ubicacion, hora_entrada, hora_salida)
    
    if updated_horario:
        return jsonify(updated_horario)
    else:
        return jsonify({'error': 'Registro no encontrado'}), 404
    

@horario_bp.route('/<int:id>', methods=['DELETE'])
def remove_horario(id):
    return delete_entrada_salida(id)

# Importar horarios
@horario_bp.route("/horarios/importar", methods=["POST"])
def importar_horarios():
    try:
        data = request.get_json()
        horarios = data.get("horarios", [])

        if not isinstance(horarios, list) or not horarios:
            return jsonify({"error": "El archivo no contiene datos válidos"}), 400

        valores = [(h["id_usuario"], h["id_ubicacion"], h["hora_entrada"], h["hora_salida"]) for h in horarios]

        sql = "INSERT INTO entradas_salidas (id_usuario, id_ubicacion, hora_entrada, hora_salida) VALUES (%s, %s, %s, %s)"
        
        with db.cursor() as cursor:
            cursor.executemany(sql, valores)
            db.commit()
            return jsonify({"mensaje": "Registros importados correctamente", "registros": cursor.rowcount})
    
    except Exception as e:
        return jsonify({"error": "Error al procesar la importación", "detalle": str(e)}), 500