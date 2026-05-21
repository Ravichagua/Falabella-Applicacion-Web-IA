from database import db

class Producto(db.Model):
    __tablename__ = 'productos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    imagen_path = db.Column(db.String(255), nullable=False)
    categoria = db.Column(db.String(80), nullable=False)
    marca = db.Column(db.String(80), nullable=False)
    
    def __repr__(self):
        return f'<Producto {self.nombre}>'
