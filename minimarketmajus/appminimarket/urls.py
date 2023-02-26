from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    #Contenido Login
    path('login', views.loginuser, name='loginuser'),
    path('logout', views.logoutuser, name='logoutuser'),

    #Contenidos Productos
    path('productos', views.productos, name='productos'),
    path('productos/crear', views.productos_crear, name='productos_crear'),
    path('productos/editar/<int:id_producto>', views.productos_editar, name='productos_editar'),
    path('productos/eliminar/<int:id_producto>', views.productos_eliminar, name='productos_eliminar'),

    #Contenido Categorias
    path('categorias', views.categorias, name='categorias'),
    path('categorias/crear', views.categorias_crear, name='categorias_crear'),
    path('categorias/editar/<int:id_categoria>', views.categorias_editar, name='categorias_editar'),
    path('categorias/eliminar/<int:id_categoria>', views.categorias_eliminar, name='categorias_eliminar'),

    #Contenido Usuario
    path('usuarios', views.usuarios, name='usuarios'),
    #Contenido ProcesoVenta
    path('procesoventa', views.procesoventa, name='procesoventa'),
    path('generar_pdf/<int:id_boleta>', views.generar_pdf, name='generar_pdf'),

    #reportes
    path('reporte', views.reporte, name='reporte'),
]

# TAREAS
# 1. (x) Hacer que funcione detalleVenta
# 2. (x) Lograr hacer funcionar el incremento/decremento de cantidad de un producto
# 3. (x) Obtener el nombre del input cliente y enviar a la base de datos
# 4. (x) Lograr que se actualice las imagenes de tanto producto y categorias
# 5. (x) Boleta
# 6. Terminar el crud de usuarios
# 7. Mejorar login (nombre dinamico)
# BONUS BONUS
# 1. Implementar la vista de reporte venta
# 2. Filtrar por categorias
# 3.Buscar a productos por codigo y (nombre opc)
# 4. Mejorar el panel principal o inicio