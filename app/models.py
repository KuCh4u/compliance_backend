from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Float, Boolean, Text, Table
from sqlalchemy.orm import relationship
from .database import Base

class Auditoria(Base):
    __tablename__ = "auditorias"
    
    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String(255), index=True)
    responsable = Column(String(100), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

class TipoUsuario(Base):
    __tablename__ = "tipos_usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String(50), unique=True, nullable=False)
    usuarios = relationship("Usuario", back_populates="tipo_usuario")

class Region(Base):
    __tablename__ = "regiones"
    
    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String(100), unique=True, nullable=False)
    clientes = relationship("Cliente", back_populates="region")

class Rubro(Base):
    __tablename__ = "rubros"
    
    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String(100), unique=True, nullable=False)
    clientes = relationship("Cliente", back_populates="rubro")

class Cliente(Base):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, index=True)
    identificador_cliente = Column(String(20), unique=True, nullable=False)
    nombre_cliente = Column(String(100), nullable=False, index=True)
    tipo_cliente = Column(String(50), nullable=False)
    tamano = Column(String(50))
    rubro_id = Column(Integer, ForeignKey("rubros.id"))
    region_id = Column(Integer, ForeignKey("regiones.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    rubro = relationship("Rubro", back_populates="clientes")
    region = relationship("Region", back_populates="clientes")
    usuarios = relationship("Usuario", back_populates="cliente")
    iniciativas = relationship("Iniciativa", back_populates="cliente")
    estandares = relationship("Estandar", secondary="cliente_estandar", back_populates="clientes")

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    tipo_usuario_id = Column(Integer, ForeignKey("tipos_usuarios.id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    nombre = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    last_login = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    tipo_usuario = relationship("TipoUsuario", back_populates="usuarios")
    cliente = relationship("Cliente", back_populates="usuarios")

class Estandar(Base):
    __tablename__ = "estandares"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre_estandar = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    controles = relationship("Control", back_populates="estandar")
    clientes = relationship("Cliente", secondary="cliente_estandar", back_populates="estandares")

class Control(Base):
    __tablename__ = "controles"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre_control = Column(String(100), nullable=False)
    id_estandar = Column(Integer, ForeignKey("estandares.id"), nullable=False)

    funcion = Column(String(150))
    categoria = Column(String(150))
    descripcion_categoria = Column(Text)
    subcategoria = Column(Text)
    escala_riesgo = Column(String(120))
    requisito_legal = Column(Text)
    ejemplo_implementación = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    estandar = relationship("Estandar", back_populates="controles")
    iniciativas = relationship("Iniciativa", back_populates="control")

class Iniciativa(Base):
    __tablename__ = "iniciativas"
    
    id = Column(Integer, primary_key=True, index=True)
    id_control = Column(Integer, ForeignKey("controles.id"), nullable=False)
    id_cliente = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    nombre_iniciativa = Column(String(100), nullable=False)
    objetivo_iniciativa = Column(Text)
    alcance_iniciativa = Column(Text)
    prioridad = Column(String(20), default="Media")  # Alta, Media, Baja
    tiempo = Column(String(50))  # O podrías usar Integer para días
    recursos = Column(Text)
    costos = Column(Float)
    cobertura = Column(String(50))
    responsable_recomendado = Column(String(100))
    fecha_inicio = Column(DateTime(timezone=True))
    fecha_fin = Column(DateTime(timezone=True))
    porcentaje_completado = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    control = relationship("Control", back_populates="iniciativas")
    cliente = relationship("Cliente", back_populates="iniciativas")

# Tabla de relación muchos-a-muchos
cliente_estandar = Table('cliente_estandar', Base.metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('cliente_id', Integer, ForeignKey('clientes.id')),
    Column('estandar_id', Integer, ForeignKey('estandares.id')),
    Column('created_at', DateTime(timezone=True), server_default=func.now())
)