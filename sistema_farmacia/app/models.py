from datetime import datetime, date
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, event, func
from sqlalchemy.orm import relationship

class Carrera(Model):
    __tablename__ = 'carrera'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), unique=True, nullable=False)
    nivel_academico = Column(String(50), nullable=False)
    duracion = Column(String(30), nullable=False)
    descripcion = Column(String(250))

    def __repr__(self):
        return self.nombre


class Alumno(Model):
    __tablename__ = 'alumno'
    id = Column(Integer, primary_key=True)
    ci = Column(String(20), unique=True, nullable=False)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    genero = Column(String(20), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    edad = Column(Integer, nullable=False, default=0)
    lugar_nacimiento = Column(String(50), nullable=False)
    telefono = Column(String(20))
    direccion = Column(String(150))
    correo_electronico = Column(String(100))
    colegio_procedencia = Column(String(100))
    
    nombre_tutor = Column(String(100), nullable=False)
    direccion_tutor = Column(String(150))
    telefono_tutor = Column(String(20))

    def __repr__(self):
        return f"{self.apellidos} {self.nombres} (CI: {self.ci})"


class Inscripcion(Model):
    __tablename__ = 'inscripcion'
    id = Column(Integer, primary_key=True)
    matricula_nro = Column(String(30), unique=True, nullable=False, default="0000")
    fecha_registro = Column(Date, default=date.today, nullable=False)
    
    alumno_id = Column(Integer, ForeignKey('alumno.id'), nullable=False)
    alumno = relationship("Alumno")
    
    carrera_id = Column(Integer, ForeignKey('carrera.id'), nullable=False)
    carrera = relationship("Carrera")

    def __repr__(self):
        return f"Matrícula: {self.matricula_nro} | {self.alumno.apellidos} {self.alumno.nombres} [{self.carrera.nombre}]"


class Pago(Model):
    __tablename__ = 'pago'
    id = Column(Integer, primary_key=True)
    monto_matricula = Column(Float, nullable=False, default=0.0)
    concepto = Column(String(100), default="Pago de Matrícula Inicial")
    fecha_pago = Column(Date, default=date.today, nullable=False)
    
    inscripcion_id = Column(Integer, ForeignKey('inscripcion.id'), nullable=False)
    inscripcion = relationship("Inscripcion")

    def __repr__(self):
        return f"Recibo {self.id} - Monto: {self.monto_matricula} Bs."


# ====================================================
# DISPARADORES AUTOMÁTICOS CORREGIDOS
# ====================================================

@event.listens_for(Alumno, 'before_insert')
@event.listens_for(Alumno, 'before_update')
def calcular_edad_al_guardar(mapper, connection, target):
    if target.fecha_nacimiento:
        hoy = date.today()
        nacimiento = target.fecha_nacimiento
        target.edad = hoy.year - nacimiento.year - ((hoy.month, hoy.day) < (nacimiento.month, nacimiento.day))

@event.listens_for(Inscripcion, 'before_insert')
def asegurar_matricula(mapper, connection, target):
    if not target.matricula_nro or target.matricula_nro in ["0000", "", None]:
        max_id = connection.execute(func.max(Inscripcion.id)).scalar()
        siguiente = 1 if max_id is None else max_id + 1
        target.matricula_nro = f"{siguiente:04d}"