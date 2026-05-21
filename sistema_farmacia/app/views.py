from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app import appbuilder, db
from .models import Categoria, Medicamento

class CategoriaView(ModelView):
    datamodel = SQLAInterface(Categoria)
    route_base = "/categorias"
    
    # Columnas que se mostrarán en la lista de la página
    list_columns = ["nombre", "descripcion"]
    
    # Etiquetas limpias para los campos de los formularios
    label_columns = {
        "nombre": "Nombre de la Categoría",
        "descripcion": "Descripción"
    }

class MedicamentoView(ModelView):
    datamodel = SQLAInterface(Medicamento)
    route_base = "/medicamentos"
    
    # Columnas visibles en la tabla principal
    list_columns = ["nombre", "precio", "stock", "fecha_vencimiento", "categoria"]
    
    # Campos que el usuario puede llenar al agregar o editar
    add_columns = ["nombre", "descripcion", "precio", "stock", "fecha_vencimiento", "categoria"]
    edit_columns = ["nombre", "descripcion", "precio", "stock", "fecha_vencimiento", "categoria"]
    
    # Etiquetas en español para la interfaz
    label_columns = {
        "nombre": "Nombre Comercial",
        "descripcion": "Descripción / Componentes",
        "precio": "Precio Unitario (Bs.)",
        "stock": "Stock Disponible",
        "fecha_vencimiento": "Fecha de Vencimiento",
        "categoria": "Categoría Fármaco"
    }

# ----------------------------------------------------
# REGISTRO EN EL MENÚ SUPERIOR
# ----------------------------------------------------

# Creamos un menú principal llamado "Gestión de Inventario"
appbuilder.add_view(
    CategoriaView,
    "Categorías de Medicamentos",
    icon="fa-folder-open",
    category="Gestión de Inventario"
)

appbuilder.add_view(
    MedicamentoView,
    "Lista de Medicamentos",
    icon="fa-flask",
    category="Gestión de Inventario"
)