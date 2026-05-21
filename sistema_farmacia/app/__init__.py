import logging
from flask import Flask
from flask_appbuilder import AppBuilder
from flask_sqlalchemy import SQLAlchemy

# Configurar el registro de logs
logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.INFO)

# Inicializar Flask
app = Flask(__name__)

# Cargar la configuración desde config.py
app.config.from_object("config")

# Inicializar la base de datos
db = SQLAlchemy(app)

# Crear el bloque de contexto para que Flask-AppBuilder funcione de forma moderna
with app.app_context():
    # Inicializar el constructor de la interfaz (AppBuilder)
    appbuilder = AppBuilder(app, db.session)

# Importar las vistas para que Flask las reconozca
from app import views