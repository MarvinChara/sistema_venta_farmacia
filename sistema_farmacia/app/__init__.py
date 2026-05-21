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

# Crear el bloque de contexto seguro
with app.app_context():
    # Inicializar el constructor de la interfaz (AppBuilder)
    appbuilder = AppBuilder(app, db.session)
    
    # Importamos los modelos para que el sistema los mapee
    from app import models
    
    # FORZADO DIRECTO RECTIFICADO: Usa el motor de 'db' para estampar las tablas en AppServ de golpe
    models.Model.metadata.create_all(bind=db.engine)
    
    # Cargamos las vistas para el menú visual
    from app import views