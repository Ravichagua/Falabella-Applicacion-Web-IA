from app import app
from database import db
from models import Producto

def init_database():
    with app.app_context():
        # Crear las tablas
        db.create_all()
        
        # Verificar si ya existen productos
        if Producto.query.first() is not None:
            print("La base de datos ya contiene productos. Omitiendo inicialización.")
            return
        
        # 10 productos
        productos = [
            Producto(
                nombre="Camiseta Clásica de Algodón",
                precio=79.99,
                descripcion="Camiseta premium elaborada con 100% algodón de alta calidad. Perfecta para el día a día.",
                imagen_path="camiseta-clasica.webp",
                categoria="Camisetas",
                marca="Nike"
            ),
            Producto(
                nombre="Pantalón Denim Azul",
                precio=119.99,
                descripcion="Pantalón de denim clásico con ajuste relajado. Combina comodidad y estilo en cualquier ocasión.",
                imagen_path="pantalon-denim.jpg",
                categoria="Pantalones",
                marca="Zara"
            ),
            Producto(
                nombre="Vestido Elegante Negro",
                precio=199.99,
                descripcion="Vestido elegante perfecto para eventos especiales. Diseño sofisticado que realza tu figura.",
                imagen_path="vestido-elegante.webp",
                categoria="Vestidos",
                marca="H&M"
            ),
            Producto(
                nombre="Chaqueta Deportiva",
                precio=349.99,
                descripcion="Chaqueta de alta calidad ideal para actividades deportivas. Material resistente y transpirable.",
                imagen_path="chaqueta-deportiva.webp",
                categoria="Chaquetas",
                marca="Adidas"
            ),
            Producto(
                nombre="Polo Básico Blanco",
                precio=59.99,
                descripcion="Polo clásico de algodón perfecto para uso casual o formal. Disponible en múltiples colores.",
                imagen_path="polo-blanco.jpg",
                categoria="Camisetas",
                marca="Ralph Lauren"
            ),
            Producto(
                nombre="Shorts de Lino",
                precio=89.99,
                descripcion="Shorts de lino cómodo y fresco para el verano. Perfectos para playa o actividades al aire libre.",
                imagen_path="shorts-lino.webp",
                categoria="Pantalones",
                marca="Uniqlo"
            ),
            Producto(
                nombre="Falda Midi Floral",
                precio=99.99,
                descripcion="Falda midi con estampado floral ideal para looks casuales y elegantes. Tela de calidad premium.",
                imagen_path="falda-mini.webp",
                categoria="Faldas",
                marca="Zara"
            ),
            Producto(
                nombre="Sudadera Hoodie Gris",
                precio=79.99,
                descripcion="Sudadera cómoda con capucha, perfecta para días frescos. Tela suave y cálida.",
                imagen_path="sudadera-hoodie.webp",
                categoria="Sudaderas",
                marca="Nike"
            ),
            Producto(
                nombre="Blazer Ejecutivo Azul",
                precio=289.99,
                descripcion="Blazer profesional ideal para ambiente corporativo. Corte impecable y material de alta calidad.",
                imagen_path="blazer-azul.jpg",
                categoria="Chaquetas",
                marca="Hugo Boss"
            ),
            Producto(
                nombre="Leggings Deportivos",
                precio=69.99,
                descripcion="Leggings de alta compresión con tecnología secado rápido. Perfectos para ejercicio.",
                imagen_path="leggings-deportivos.webp",
                categoria="Pantalones",
                marca="Adidas"
            ),
        ]
        
        # Agregar los productos a la sesión
        for producto in productos:
            db.session.add(producto)
        
        # Hacer commit de los cambios
        db.session.commit()
        print("Base de datos inicializada con 10 productos exitosamente!")

if __name__ == '__main__':
    init_database()
