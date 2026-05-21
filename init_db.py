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
                imagen_path="https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop",
                categoria="Camisetas",
                marca="Nike"
            ),
            Producto(
                nombre="Pantalón Denim Azul",
                precio=119.99,
                descripcion="Pantalón de denim clásico con ajuste relajado. Combina comodidad y estilo en cualquier ocasión.",
                imagen_path="https://images.unsplash.com/photo-1548126033-3080ca022206?w=400&h=400&fit=crop",
                categoria="Pantalones",
                marca="Zara"
            ),
            Producto(
                nombre="Vestido Elegante Negro",
                precio=199.99,
                descripcion="Vestido elegante perfecto para eventos especiales. Diseño sofisticado que realza tu figura.",
                imagen_path="https://images.unsplash.com/photo-1503342394128-c104cbb9810d?w=400&h=400&fit=crop",
                categoria="Vestidos",
                marca="H&M"
            ),
            Producto(
                nombre="Chaqueta Deportiva",
                precio=349.99,
                descripcion="Chaqueta de alta calidad ideal para actividades deportivas. Material resistente y transpirable.",
                imagen_path="https://images.unsplash.com/photo-1551028719-00167b16ebc5?w=400&h=400&fit=crop",
                categoria="Chaquetas",
                marca="Adidas"
            ),
            Producto(
                nombre="Polo Básico Blanco",
                precio=59.99,
                descripcion="Polo clásico de algodón perfecto para uso casual o formal. Disponible en múltiples colores.",
                imagen_path="https://images.unsplash.com/photo-1577992369052-f59d99b47a91?w=400&h=400&fit=crop",
                categoria="Camisetas",
                marca="Ralph Lauren"
            ),
            Producto(
                nombre="Shorts de Lino",
                precio=89.99,
                descripcion="Shorts de lino cómodo y fresco para el verano. Perfectos para playa o actividades al aire libre.",
                imagen_path="https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=400&h=400&fit=crop",
                categoria="Pantalones",
                marca="Uniqlo"
            ),
            Producto(
                nombre="Falda Midi Floral",
                precio=99.99,
                descripcion="Falda midi con estampado floral ideal para looks casuales y elegantes. Tela de calidad premium.",
                imagen_path="https://images.unsplash.com/photo-1606308790433-f47ddba9f9f8?w=400&h=400&fit=crop",
                categoria="Faldas",
                marca="Zara"
            ),
            Producto(
                nombre="Sudadera Hoodie Gris",
                precio=79.99,
                descripcion="Sudadera cómoda con capucha, perfecta para días frescos. Tela suave y cálida.",
                imagen_path="https://images.unsplash.com/photo-1556821552-5e41911c0e8d?w=400&h=400&fit=crop",
                categoria="Sudaderas",
                marca="Nike"
            ),
            Producto(
                nombre="Blazer Ejecutivo Azul",
                precio=289.99,
                descripcion="Blazer profesional ideal para ambiente corporativo. Corte impecable y material de alta calidad.",
                imagen_path="https://images.unsplash.com/photo-1539533057440-7bc282412ba2?w=400&h=400&fit=crop",
                categoria="Chaquetas",
                marca="Hugo Boss"
            ),
            Producto(
                nombre="Leggings Deportivos",
                precio=69.99,
                descripcion="Leggings de alta compresión con tecnología secado rápido. Perfectos para ejercicio.",
                imagen_path="https://images.unsplash.com/photo-1506215316815-2da0b1f0d545?w=400&h=400&fit=crop",
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
