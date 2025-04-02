from flask import Flask, jsonify
from config import db, migrate
from dotenv import load_dotenv
from sqlalchemy import text
import os
from routes.user import user_bp
from routes.horarios import horario_bp
from routes.ubi import ubicacion_bp
from flask_cors import CORS
from flask_jwt_extended import JWTManager
load_dotenv()

app = Flask(__name__) 
CORS(app)
app.config['JWT_SECRET_KEY'] = 'Hoy desperte con ganas'
jwt = JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate.init_app(app, db)


app.register_blueprint(user_bp, url_prefix='/usuarios')
app.register_blueprint(horario_bp, url_prefix='/horarios')
app.register_blueprint(ubicacion_bp, url_prefix='/ubicacion')

if __name__ == '__main__':
    app.run(debug=True)