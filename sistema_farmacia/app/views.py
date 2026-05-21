from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app import appbuilder, db
from .models import Categoria, Medicamento, Venta, DetalleVenta

# ----------------------------------------------------
# VISTAS DE INVENTARIO
# ----------------------------------------------------

class CategoriaView(ModelView):
    datamodel = SQLAInterface(Categoria)
    route_base = "/categorias"
    list_columns = ["nombre", "descripcion"]
    label_columns = {
        "nombre": "Nombre de la Categoría",
        "descripcion": "Descripción"
    }

class MedicamentoView(ModelView):
    datamodel = SQLAInterface(Medicamento)
    route_base = "/medicamentos"
    list_columns = ["nombre", "precio", "stock", "fecha_vencimiento", "categoria"]
    add_columns = ["nombre", "descripcion", "precio", "stock", "fecha_vencimiento", "categoria"]
    edit_columns = ["nombre", "descripcion", "precio", "stock", "fecha_vencimiento", "categoria"]
    label_columns = {
        "nombre": "Nombre Comercial",
        "descripcion": "Descripción / Componentes",
        "precio": "Precio Unitario (Bs.)",
        "stock": "Stock Disponible",
        "fecha_vencimiento": "Fecha de Vencimiento",
        "categoria": "Categoría Fármaco"
    }

# ----------------------------------------------------
# VISTAS DE VENTAS (AUTOMATIZADAS)
# ----------------------------------------------------

class DetalleVentaView(ModelView):
    datamodel = SQLAInterface(DetalleVenta)
    route_base = "/detalles_ventas"
    
    list_columns = ["venta", "medicamento", "cantidad", "precio_unitario", "subtotal"]
    
    # HABILITADO 'precio_unitario': Ahora puedes escribir un precio con descuento aquí.
    # 'subtotal' se queda oculto porque se calculará solo matemáticamente.
    add_columns = ["venta", "medicamento", "cantidad", "precio_unitario"]
    edit_columns = ["venta", "medicamento", "cantidad", "precio_unitario"]
    
    label_columns = {
        "venta": "Factura Nro.",
        "medicamento": "Medicamento Seleccionado",
        "cantidad": "Cantidad Vendida",
        "precio_unitario": "Precio de Venta (Bs.) [Dejar en 0 para usar precio base]",
        "subtotal": "Subtotal Calculado (Bs.)"
    }

class VentaView(ModelView):
    datamodel = SQLAInterface(Venta)
    route_base = "/ventas"
    
    # En la lista vemos el ID de factura, la fecha y el gran total acumulado solo
    list_columns = ["id", "fecha", "total"]
    
    # ¡QUEDANTE OCULTO EL TOTAL!: Se inicializa en 0.0 y sube solo a medida que agregues ítems
    add_columns = ["fecha"]
    edit_columns = ["fecha"]
    
    label_columns = {
        "id": "Nro. de Factura / Venta",
        "fecha": "Fecha de Registro",
        "total": "Total de la Venta (Bs.)"
    }

# ----------------------------------------------------
# REGISTRO EN EL MENÚ SUPERIOR
# ----------------------------------------------------

# Menú 1: Gestión de Inventario
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

# Menú 2: Módulo de Ventas
appbuilder.add_view(
    VentaView,
    "1. Cabecera de Ventas",
    icon="fa-shopping-cart",
    category="Módulo de Ventas"
)

appbuilder.add_view(
    DetalleVentaView,
    "2. Cargar Items (Detalle)",
    icon="fa-plus-circle",
    category="Módulo de Ventas"
)