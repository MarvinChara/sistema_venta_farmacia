import datetime
from flask_appbuilder import Model
from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric, String, ForeignKey, Text
from sqlalchemy.orm import relationship

class Categoria(Model):
    __tablename__ = "categoria"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text, nullable=True)

    # RELACIÓN: Una categoría tiene muchos medicamentos
    medicamentos = relationship(
        "Medicamento",
        back_populates="categoria",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return self.nombre


class Medicamento(Model):
    __tablename__ = "medicamento"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    fecha_vencimiento = Column(DateTime, nullable=True)
    categoria_id = Column(Integer, ForeignKey("categoria.id"), nullable=False)

    # RELACIÓN: Muchos medicamentos pertenecen a una categoría
    categoria = relationship(
        "Categoria",
        back_populates="medicamentos"
    )
    
    # RELACIÓN: Un medicamento puede aparecer en muchos detalles de ventas
    detalles = relationship(
        "DetalleVenta",
        back_populates="medicamento"
    )

    def __repr__(self):
        return f"{self.nombre} (P. Unit: {self.precio} Bs.)"


class Venta(Model):
    __tablename__ = "venta"
    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    total = Column(Numeric(10, 2), nullable=False, default=0.00)

    # RELACIÓN: Una venta tiene muchos detalles (productos comprados)
    detalles = relationship(
        "DetalleVenta",
        back_populates="venta",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Venta #{self.id} - Fecha: {self.fecha.strftime('%d/%m/%Y')} - Total: {self.total} Bs."


class DetalleVenta(Model):
    __tablename__ = "detalle_venta"
    id = Column(Integer, primary_key=True)
    venta_id = Column(Integer, ForeignKey("venta.id"), nullable=False)
    medicamento_id = Column(Integer, ForeignKey("medicamento.id"), nullable=False)
    cantidad = Column(Integer, nullable=False, default=1)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)

    # RELACIÓN: Muchos detalles pertenecen a una sola Venta
    venta = relationship(
        "Venta",
        back_populates="detalles"
    )
    
    # RELACIÓN: Muchos detalles apuntan a un Medicamento
    medicamento = relationship(
        "Medicamento",
        back_populates="detalles"
    )

    def __repr__(self):
        return f"Detalle #{self.id} - Cantidad: {self.cantidad}"