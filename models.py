from database import db
from werkzeug.security import generate_password_hash, check_password_hash

class Producto(db.Model):
    __tablename__ = 'productos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    imagen_path = db.Column(db.String(255), nullable=False)
    categoria = db.Column(db.String(80), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    marca = db.Column(db.String(80), nullable=False)
    
    def __repr__(self):
        return f'<Producto {self.nombre}>'


class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default='usuario')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Usuario {self.email} ({self.rol})>'


class Deseado(db.Model):
    __tablename__ = 'deseados'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)

    usuario = db.relationship('Usuario', backref=db.backref('deseados', lazy=True, cascade='all, delete-orphan'))
    producto = db.relationship('Producto', backref=db.backref('deseados', lazy=True, cascade='all, delete-orphan'))

    __table_args__ = (
        db.UniqueConstraint('usuario_id', 'producto_id', name='uq_deseados_usuario_producto'),
    )

    def __repr__(self):
        return f'<Deseado usuario={self.usuario_id} producto={self.producto_id}>'
