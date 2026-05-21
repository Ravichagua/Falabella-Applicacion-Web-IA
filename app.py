from flask import Flask, render_template, jsonify, redirect, url_for # type: ignore
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()

app = Flask(__name__)

# Configuración de la base de datos (solo PostgreSQL)
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise RuntimeError("DATABASE_URL no definida. Añade DATABASE_URL con la URI de PostgreSQL en el entorno o en .env")
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from database import db
db.init_app(app)

# Importar modelos
from models import Producto

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/busqueda")
def busqueda():
    productos = Producto.query.all()
    return render_template("busqueda.html", productos=productos)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/detalle")
def detalle_default():
    primer_producto = Producto.query.order_by(Producto.id.asc()).first()
    if primer_producto is None:
        return redirect(url_for('busqueda'))
    return redirect(url_for('detalle', producto_id=primer_producto.id))


@app.route("/detalle/<int:producto_id>")
def detalle(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    relacionados = (
        Producto.query
        .filter(Producto.id != producto.id)
        .limit(4)
        .all()
    )
    return render_template("detalle.html", producto=producto, relacionados=relacionados)

@app.route("/api/productos")
def api_productos():
    productos = Producto.query.all()
    return jsonify([{
        'id': p.id,
        'nombre': p.nombre,
        'precio': p.precio,
        'descripcion': p.descripcion,
        'imagen_path': p.imagen_path,
        'categoria': p.categoria,
        'marca': p.marca
    } for p in productos])


if __name__ == "__main__":
    app.run(debug=True)