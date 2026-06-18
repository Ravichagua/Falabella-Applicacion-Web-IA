from flask import Flask, render_template, jsonify, redirect, url_for, request, session # type: ignore
from dotenv import load_dotenv
import os
from werkzeug.utils import secure_filename

# Cargar variables de entorno desde .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

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

# Carpeta donde se guardan las imágenes de productos
PRODUCTOS_FOLDER = os.path.join(app.root_path, 'static', 'imagenes', 'productos')
os.makedirs(PRODUCTOS_FOLDER, exist_ok=True)

# Importar modelos
from models import Deseado, Producto, Usuario

# Iniciar base de datos (el módulo contiene la función `init_database`)
import init_db


# Rutas
@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.check_password(password):
            session["usuario_id"] = usuario.id
            session["usuario"] = usuario.email
            session["rol"] = usuario.rol
            if usuario.rol == "admin":
                return redirect(url_for("dashboard"))
            return redirect(url_for("busqueda"))

        return render_template(
            "login.html",
            error="Credenciales inválidas. Intenta de nuevo."
        )

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


def _usuario_autenticado():
    return session.get("rol") in {"usuario", "admin"} and session.get("usuario_id") is not None

@app.route("/busqueda")
def busqueda():
    if session.get("rol") not in {"usuario", "admin"}:
        return redirect(url_for("login"))

    termino_busqueda = request.args.get("q", "").strip()
    precio_max_param = request.args.get("precio_max", "").strip()
    categorias_seleccionadas = request.args.getlist("categoria")
    marcas_seleccionadas = request.args.getlist("marca")
    precio_max = 1000

    if precio_max_param:
        try:
            precio_max = int(precio_max_param)
        except ValueError:
            precio_max = 1000

    # Limita el valor para mantenerlo dentro del rango del slider.
    precio_max = max(10, min(precio_max, 1000))

    consulta_productos = Producto.query

    # La busqueda solo considera el nombre del producto.
    if termino_busqueda:
        consulta_productos = consulta_productos.filter(
            Producto.nombre.ilike(f"%{termino_busqueda}%")
        )

    if categorias_seleccionadas:
        consulta_productos = consulta_productos.filter(
            Producto.categoria.in_(categorias_seleccionadas)
        )

    if marcas_seleccionadas:
        consulta_productos = consulta_productos.filter(
            Producto.marca.in_(marcas_seleccionadas)
        )

    consulta_productos = consulta_productos.filter(Producto.precio <= precio_max)

    productos = consulta_productos.all()
    categorias_disponibles = [
        categoria
        for (categoria,) in db.session.query(Producto.categoria)
        .distinct()
        .order_by(Producto.categoria.asc())
        .all()
    ]
    marcas_disponibles = [
        marca
        for (marca,) in db.session.query(Producto.marca)
        .distinct()
        .order_by(Producto.marca.asc())
        .all()
    ]

    return render_template(
        "busqueda.html",
        productos=productos,
        termino_busqueda=termino_busqueda,
        precio_max=precio_max,
        categorias_disponibles=categorias_disponibles,
        marcas_disponibles=marcas_disponibles,
        categorias_seleccionadas=categorias_seleccionadas,
        marcas_seleccionadas=marcas_seleccionadas,
    )

@app.route("/deseados")
def deseados():
    if session.get("rol") != "usuario" or session.get("usuario_id") is None:
        return redirect(url_for("login"))

    lista_deseados = (
        Deseado.query
        .filter_by(usuario_id=session["usuario_id"])
        .join(Producto)
        .order_by(Deseado.id.desc())
        .all()
    )
    return render_template("listaDeseados.html", lista_deseados=lista_deseados)


@app.route("/deseados/agregar/<int:producto_id>", methods=["POST"])
def agregar_deseado(producto_id):
    if session.get("rol") != "usuario" or session.get("usuario_id") is None:
        return redirect(url_for("login"))

    producto = Producto.query.get_or_404(producto_id)
    deseado_existente = Deseado.query.filter_by(
        usuario_id=session["usuario_id"],
        producto_id=producto.id,
    ).first()

    if deseado_existente is None:
        db.session.add(Deseado(usuario_id=session["usuario_id"], producto_id=producto.id))
        db.session.commit()

    return redirect(request.referrer or url_for("deseados"))


@app.route("/deseados/<int:deseado_id>/eliminar", methods=["POST"])
def eliminar_deseado(deseado_id):
    if session.get("rol") != "usuario" or session.get("usuario_id") is None:
        return redirect(url_for("login"))

    deseado = Deseado.query.filter_by(id=deseado_id, usuario_id=session["usuario_id"]).first_or_404()
    db.session.delete(deseado)
    db.session.commit()
    return redirect(url_for("deseados"))

@app.route("/dashboard")
def dashboard():
    if session.get("rol") != "admin":
        return redirect(url_for("login"))
    # Contadores para el dashboard
    try:
        productos_count = Producto.query.count()
    except Exception:
        productos_count = 0

    try:
        deseados_count = Deseado.query.count()
    except Exception:
        deseados_count = 0

    return render_template("dashboard.html", productos_count=productos_count, deseados_count=deseados_count)

@app.route("/dashboard/inventario", methods=["GET", "POST"])
def gestionInventario():
    if session.get("rol") != "admin":
        return redirect(url_for("login"))

    error = None
    # POST productos
    if request.method == "POST":
        producto_id = request.form.get("producto_id", type=int)
        nombre = request.form.get("nombre", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        # Manejo de archivo subido (opcional) y nombre de imagen
        imagen_file = request.files.get('imagen_file')
        imagen_path = request.form.get("imagen_path", "").strip()

        if imagen_file and imagen_file.filename:
            filename = secure_filename(imagen_file.filename)
            try:
                imagen_file.save(os.path.join(PRODUCTOS_FOLDER, filename))
                imagen_path = filename
            except Exception:
                error = "No se pudo guardar la imagen subida."
        categoria = request.form.get("categoria", "").strip()
        marca = request.form.get("marca", "").strip()

        try:
            precio = float(request.form.get("precio", "0").strip())
            stock = int(request.form.get("stock", "0").strip())
        except ValueError:
            error = "Precio y stock deben ser números válidos."
        else:
            if not all([nombre, descripcion, categoria, marca]):
                error = "Completa todos los campos del producto."
            elif not imagen_path:
                error = "Agrega una imagen para el producto."
            else:
                try:
                    if producto_id:
                        producto = Producto.query.get_or_404(producto_id)
                        producto.nombre = nombre
                        producto.precio = precio
                        producto.descripcion = descripcion
                        producto.imagen_path = imagen_path
                        producto.categoria = categoria
                        producto.stock = stock
                        producto.marca = marca
                    else:
                        producto = Producto(
                            nombre=nombre,
                            precio=precio,
                            descripcion=descripcion,
                            imagen_path=imagen_path,
                            categoria=categoria,
                            stock=stock,
                            marca=marca,
                        )
                        db.session.add(producto)

                    db.session.commit()
                    return redirect(url_for("gestionInventario"))
                except Exception:
                    db.session.rollback()
                    error = "No se pudo guardar el producto. Revisa los datos e inténtalo de nuevo."

    editar_id = request.args.get("editar", type=int)
    producto_edicion = Producto.query.get_or_404(editar_id) if editar_id else None
    productos = Producto.query.all()
    return render_template(
        "gestionInventario.html",
        productos=productos,
        producto_edicion=producto_edicion,
        error=error,
    )


@app.route("/dashboard/inventario/<int:producto_id>/eliminar", methods=["POST"])
def eliminar_producto(producto_id):
    if session.get("rol") != "admin":
        return redirect(url_for("login"))

    producto = Producto.query.get_or_404(producto_id)
    db.session.delete(producto)
    db.session.commit()
    return redirect(url_for("gestionInventario"))

@app.route("/dashboard/usuarios", methods=["GET", "POST"])
def gestionUsuario():
    if session.get("rol") != "admin":
        return redirect(url_for("login"))

    error = None

    if request.method == "POST":
        usuario_id = request.form.get("usuario_id", type=int)
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        rol = request.form.get("rol", "usuario")

        if rol not in {"usuario", "admin"}:
            error = "El rol seleccionado no es válido."
        elif not all([nombre, email]):
            error = "Nombre y correo son obligatorios."
        elif not usuario_id and not password:
            error = "La contraseña es obligatoria para un usuario nuevo."
        else:
            usuario_existente = Usuario.query.filter(Usuario.email == email)
            if usuario_id:
                usuario_existente = usuario_existente.filter(Usuario.id != usuario_id)

            if usuario_existente.first() is not None:
                error = "Ya existe un usuario con ese correo."
            else:
                try:
                    if usuario_id:
                        usuario = Usuario.query.get_or_404(usuario_id)
                        usuario.nombre = nombre
                        usuario.email = email
                        usuario.rol = rol
                        if password:
                            usuario.set_password(password)
                    else:
                        usuario = Usuario(nombre=nombre, email=email, rol=rol)
                        usuario.set_password(password)
                        db.session.add(usuario)

                    db.session.commit()
                    return redirect(url_for("gestionUsuario"))
                except Exception:
                    db.session.rollback()
                    error = "No se pudo guardar el usuario. Revisa los datos e inténtalo de nuevo."

    editar_usuario_id = request.args.get("editar", type=int)
    usuario_edicion = Usuario.query.get_or_404(editar_usuario_id) if editar_usuario_id else None
    usuarios_normales = Usuario.query.filter_by(rol="usuario").order_by(Usuario.nombre.asc()).all()
    usuarios_admin = Usuario.query.filter_by(rol="admin").order_by(Usuario.nombre.asc()).all()
    return render_template(
        "gestionUsuario.html",
        usuarios_normales=usuarios_normales,
        usuarios_admin=usuarios_admin,
        usuario_edicion=usuario_edicion,
        error=error,
    )


@app.route("/dashboard/usuarios/<int:usuario_id>/eliminar", methods=["POST"])
def eliminar_usuario(usuario_id):
    if session.get("rol") != "admin":
        return redirect(url_for("login"))

    usuario = Usuario.query.get_or_404(usuario_id)
    if usuario.email == session.get("usuario"):
        return redirect(url_for("gestionUsuario"))

    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for("gestionUsuario"))

@app.route("/detalle")
def detalle_default():
    primer_producto = Producto.query.order_by(Producto.id.asc()).first()
    if primer_producto is None:
        return redirect(url_for('busqueda'))
    return redirect(url_for('detalle', producto_id=primer_producto.id))


@app.route("/detalle/<int:producto_id>")
def detalle(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    es_deseado = False
    if session.get("usuario_id") is not None:
        es_deseado = Deseado.query.filter_by(
            usuario_id=session["usuario_id"],
            producto_id=producto.id,
        ).first() is not None

    relacionados = (
        Producto.query
        .filter(Producto.id != producto.id)
        .limit(4)
        .all()
    )
    return render_template("detalle.html", producto=producto, relacionados=relacionados, es_deseado=es_deseado)

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
        'stock': p.stock,
        'marca': p.marca
    } for p in productos])



# Inicio
if __name__ == "__main__":
    # Inicializar la base de datos dentro del app context antes de arrancar
    init_db.init_database()
    app.run(debug=True)