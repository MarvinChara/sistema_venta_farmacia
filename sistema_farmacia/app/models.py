from datetime import datetime
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
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
        return self.nombre

class Venta(Model):
    __tablename__ = 'venta'
    id = Column(Integer, primary_key=True)
    fecha = Column(Date, default=datetime.utcnow, nullable=False)
    total = Column(Float, default=0.0)

    def __repr__(self):
        return f"Venta Nro {self.id} - {self.fecha}"

class DetalleVenta(Model):
    __tablename__ = 'detalle_venta'
    id = Column(Integer, primary_key=True)
    venta_id = Column(Integer, ForeignKey('venta.id'), nullable=False)
    medicamento_id = Column(Integer, ForeignKey('medicamento.id'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    venta = relationship("Venta")
    medicamento = relationship("Medicamento")