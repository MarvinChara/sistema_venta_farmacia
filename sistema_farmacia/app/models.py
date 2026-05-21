from datetime import datetime
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, event
from sqlalchemy.orm import relationship

class Categoria(Model):
    __tablename__ = 'categoria'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(String(250))

    def __repr__(self):
        return self.nombre

class Medicamento(Model):
    __tablename__ = 'medicamento'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(250))
    precio = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    
    categoria_id = Column(Integer, ForeignKey('categoria.id'), nullable=False)
    categoria = relationship("Categoria")

    def __repr__(self):
        return f"{self.nombre} (Stock: {self.stock} | Precio: {self.precio} Bs.)"

class Venta(Model):
    __tablename__ = 'venta'
    id = Column(Integer, primary_key=True)
    fecha = Column(Date, default=datetime.utcnow, nullable=False)
    total = Column(Float, default=0.0)
    
    # Relación inversa para poder sumar los detalles fácilmente
    detalles = relationship("DetalleVenta", back_populates="venta", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Factura Nro {self.id} - {self.fecha} (Total: {self.total} Bs.)"

class DetalleVenta(Model):
    __tablename__ = 'detalle_venta'
    id = Column(Integer, primary_key=True)
    venta_id = Column(Integer, ForeignKey('venta.id'), nullable=False)
    medicamento_id = Column(Integer, ForeignKey('medicamento.id'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, default=0.0)
    subtotal = Column(Float, default=0.0)

    venta = relationship("Venta", back_populates="detalles")
    medicamento = relationship("Medicamento")

    def __repr__(self):
        return f"Item {self.id} - Cantidad: {self.cantidad}"


# ====================================================
# DISPARADORES / EVENTOS AUTOMÁTICOS (LOGICA DE NEGOCIO)
# ====================================================

@event.listens_for(DetalleVenta, 'before_insert')
@event.listens_for(DetalleVenta, 'before_update')
def calcular_subtotal_y_descontar_stock(mapper, connection, target):
    """
    Antes de guardar el detalle:
    1. Si el usuario NO especificó un precio manual, jala el precio base del medicamento.
    2. Calcula el subtotal basándose en el precio final (que puede ser modificado).
    3. Resta la cantidad vendida del stock disponible.
    """
    # 1. Obtener los datos actuales del medicamento
    medicamento = connection.execute(
        Medicamento.__table__.select().where(Medicamento.__table__.c.id == target.medicamento_id)
    ).fetchone()
    
    if medicamento:
        # LÓGICA DE PRECIO MODIFICABLE: 
        # Si el usuario no escribió un precio (es None o 0), usamos el precio de lista.
        # Si escribió algo (ej: aplicó un descuento), respetamos su precio manual.
        if target.precio_unitario is None or float(target.precio_unitario) == 0.0:
            target.precio_unitario = medicamento.precio
            
        # 2. Calcular el subtotal con el precio definitivo
        target.subtotal = float(target.cantidad) * float(target.precio_unitario)
        
        # 3. Restar del stock físico
        nuevo_stock = medicamento.stock - target.cantidad
        connection.execute(
            Medicamento.__table__.update().
            where(Medicamento.__table__.c.id == target.medicamento_id).
            values(stock=nuevo_stock)
        )

def actualizar_total_venta(connection, venta_id):
    """ Función auxiliar para sumar todos los subtotales de una factura """
    # Sumar todos los subtotales correspondientes a la venta_id
    resultado = connection.execute(
        DetalleVenta.__table__.select().where(DetalleVenta.__table__.c.venta_id == venta_id)
    ).fetchall()
    
    gran_total = sum(float(fila.subtotal) for fila in resultado)
    
    # Actualizar el campo 'total' de la cabecera (Venta)
    connection.execute(
        Venta.__table__.update().
        where(Venta.__table__.c.id == venta_id).
        values(total=gran_total)
    )

@event.listens_for(DetalleVenta, 'after_insert')
@event.listens_for(DetalleVenta, 'after_update')
@event.listens_for(DetalleVenta, 'after_delete')
def disparar_actualizacion_total(mapper, connection, target):
    """ Después de cualquier cambio en los detalles, recalcula el total de la factura """
    actualizar_total_venta(connection, target.venta_id)