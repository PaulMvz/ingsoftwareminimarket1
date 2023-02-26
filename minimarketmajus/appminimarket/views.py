from datetime import datetime
from django.shortcuts import render, redirect
from appminimarket.models import Categoria, Producto, Usuario, Boleta,DetalleBoleta
from django.http import HttpResponse

from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.decorators import login_required

#importando para poder subir imagenes al servidor
from django.core.files.storage import FileSystemStorage

from django.template.loader import get_template
from weasyprint import HTML, CSS

from django.db.models import Sum

# Create your views here.

### INDEX::BEGIN ###
@login_required()
def index(request):
    total_usuarios = Usuario.objects.all().count()
    total_productos = Producto.objects.all().count()
    cantidad_boletas = Boleta.objects.all().count()
    total_ventas = Boleta.objects.aggregate(Sum('total_ventas'))
    total_ventas = total_ventas['total_ventas__sum']
    return render(request, 'index.html', {
        'total_usuarios':total_usuarios,
        'total_productos': total_productos,
        'cantidad_boletas': cantidad_boletas,
        'total_ventas':total_ventas,
        })
### INDEX::END ###


### LOGIN::BEGIN ###
def loginuser(request):
    try:
        if request.method == 'POST':
            username1 = request.POST['username']
            password1 = request.POST['password']
            user = authenticate(request, username = username1, password = password1)
            if user is not None:
                # si el usuario existe
                login(request, user)
                request.session['nombre_usuario'] = Usuario.objects.get(id_usuario=user.id).nombre_usuario
                return redirect('index')
            else:
                mensaje = "Contraseña y usuario incorrecto"
                return render(request, 'login/login.html',{'mensaje':mensaje})
        else:
            return render(request, 'login/login.html')
    except Exception as e:
        return HttpResponse("Error al obtener los datos del Usuario - " + str(e))
def logoutuser(request):
    logout(request)
    return redirect('loginuser')
### LOGIN::END ###

### PRODUCTOS::BEGIN ###
@login_required()
def productos(request):
    try:
        productos = Producto.objects.all()
        return render(request, "productos/productos.html", {'productos':productos})
    except Exception as e:
        return HttpResponse("Error al obtener los datos de los productos - " + str(e))
@login_required()
def productos_crear(request):
    try:
        if request.method == 'POST':
            producto = Producto()
            producto.codigo_producto = request.POST['codigo_producto']
            producto.nombre_producto = request.POST['nombre_producto']
            producto.descripcion_producto = request.POST['descripcion_producto']
            producto.cant_stock_producto = request.POST['cant_stock_producto']
            producto.precio_producto = request.POST['precio_producto']
            producto.id_categoria = Categoria.objects.get(id_categoria=request.POST['id_categoria'])
            if request.FILES != {}: # si se envio el archivo
                if request.FILES['imagen_producto']:
                    logo = request.FILES['imagen_producto']
                    fs = FileSystemStorage()
                    fs.save(f'Productos/{logo.name}', logo)
                    producto.imagen_producto = f'Productos/{logo.name}'
            else:
                producto.imagen_producto = 'Productos/default.png'
            producto.save()
            return redirect('productos')
        else:
            categorias = Categoria.objects.all()
            return render(request, "productos/crear.html", {'categorias':categorias})
    except Exception as e:
        return HttpResponse("Error al obtener los datos de los productos - " + str(e))
@login_required()
def productos_editar(request, id_producto):
    try:
        producto = Producto.objects.get(id_producto = id_producto)
        if request.method == 'POST':
            producto.codigo_producto = request.POST['codigo_producto']
            producto.nombre_producto = request.POST['nombre_producto']
            producto.descripcion_producto = request.POST['descripcion_producto']
            producto.cant_stock_producto = request.POST['cant_stock_producto']
            #producto.imagen_producto = request.POST['imagen_producto']
            producto.precio_producto = request.POST['precio_producto']
            producto.id_categoria = Categoria.objects.get(id_categoria=request.POST['id_categoria'])
            if request.FILES != {}:
                if request.FILES['imagen_producto']:
                    fs = FileSystemStorage()
                    if producto.imagen_producto.name != 'default.png':
                        logo_anterior = producto.imagen_producto.name
                        fs.delete(logo_anterior)
                    logo_nuevo = request.FILES['imagen_producto']
                    fs.save(f'Productos/{logo_nuevo.name}',logo_nuevo)
                    producto.imagen_producto = f'Productos/{logo_nuevo.name}'
            producto.save()
            return redirect('productos')
        else:
            categorias = Categoria.objects.all()
            return render(request,"productos/editar.html",{'producto':producto,'categorias':categorias})
    except Exception as e:
        return HttpResponse("Error al obtener los datos de los productos - " + str(e))
@login_required()
def productos_eliminar(request, id_producto):
    try:
        producto = Producto.objects.get(id_producto = id_producto)
        logo = producto.imagen_producto.name
        if logo != 'Productos/default.png':
            fs = FileSystemStorage()
            fs.delete(logo)
        producto.delete()
        return redirect('productos')
    except Exception as e:
        return HttpResponse("Error al obtener los datos de los productos - " + str(e))
### PRODUCTOS::END ###

### CATEGORIAS::BEGIN ###
@login_required()
def categorias(request):
    try:
        categorias = Categoria.objects.all()
        return render(request, "categorias/categorias.html",{'categorias':categorias})
    except Exception as e:
         return HttpResponse("Error al obtener los datos de las categorias - " + str(e))
@login_required()
def categorias_crear(request):
    try:
        if request.method == 'POST': #POST
            # recepcionar datos
            categoria = Categoria()
            categoria.nombre_categoria = request.POST['nombre_categoria']
            if request.FILES != {}: # si se envio el archivo
                if request.FILES['imagen_categoria']:
                    logo = request.FILES['imagen_categoria']
                    fs = FileSystemStorage()
                    fs.save(f'Categorias/{logo.name}', logo)
                    categoria.imagen_categoria = f'Categorias/{logo.name}'
            else:
                categoria.imagen_categoria = 'Categorias/default.png'
            categoria.save()
            return redirect('categorias')
        else: # GET
            return render(request, "categorias/crear.html")
    except Exception as e:
        return HttpResponse("Error al obtener los datos de las categorias - " + str(e))
@login_required()
def categorias_editar(request, id_categoria):
    try:
        categoria = Categoria.objects.get(id_categoria = id_categoria)
        if request.method == 'POST': 
            # Actualizar el registro con el id
            categoria.nombre_categoria = request.POST['nombre_categoria']
            if request.FILES != {}:
                if request.FILES['imagen_categoria']:
                    fs = FileSystemStorage()
                    if categoria.imagen_categoria.name != 'default.png':
                        logo_anterior = categoria.imagen_categoria.name
                        fs.delete(logo_anterior)
                    logo_nuevo = request.FILES['imagen_categoria']
                    fs.save(f'Categorias/{logo_nuevo.name}',logo_nuevo)
                    categoria.imagen_categoria = f'Categorias/{logo_nuevo.name}'
            categoria.save()
            return redirect('categorias')
        else:
            # obtener el registro mediante el id y mostrarlo
            return render(request, "categorias/editar.html", {'categoria':categoria})
    except Exception as e:
        return HttpResponse("Error al obtener los datos de las categorias - " + str(e))
@login_required()
def categorias_eliminar(request, id_categoria):
    try:
        # eliminar el registro actualizar la lista
        categoria = Categoria.objects.get(id_categoria = id_categoria)
        logo = categoria.imagen_categoria.name
        if logo != 'Categorias/default.png':
            fs = FileSystemStorage()
            fs.delete(logo)
        categoria.delete()
        return redirect('categorias')
    except Exception as e:
        return HttpResponse("Error al obtener los datos de las categorias - " + str(e))
### CATEGORIAS::END ###

### USUARIO::BEGIN ###
@login_required()
def usuarios(request):
    try:
        usuarios = Usuario.objects.all()
        return render(request, "usuarios/usuarios.html", {'usuarios':usuarios})
    except Exception as e:
        return HttpResponse("Error al obtener los datos de los usuarios- " + str(e))    
### USUARIO::END ###

### PROCESOVENTA::BEGIN ###
@login_required()
def procesoventa(request):
    try:
        if request.method == 'POST':
            id_producto_xyz = request.POST['id_producto_xyz']
            cantidad_detalleboleta_xyz = request.POST['cantidad_detalleboleta_xyz']
            totalVentas = 0

            boleta = Boleta()
            boleta.id_usuario = Usuario.objects.get(id_usuario = '1')
            boleta.nombrecliente_boleta = request.POST['nombre_cliente_server']
            boleta.fecha_boleta = datetime.now()
            boleta.save()
            # convertir en lista los id de productos
            id_producto = []
            for i in id_producto_xyz.split(','):
                id_producto.append(int(i))
            # convertir en lista las cantidades de productos
            cantidad_detalleboleta = []
            for i in cantidad_detalleboleta_xyz.split(','):
                cantidad_detalleboleta.append(int(i))
            # recorrer la lista de id de productos
            for i in range(len(id_producto)):
                precioUnitario = Producto.objects.get(id_producto = id_producto[i]).precio_producto
                cantidad = cantidad_detalleboleta[i]
                subTotal = float(cantidad)*float(precioUnitario)

                detalleBoleta = DetalleBoleta()
                detalleBoleta.id_producto = Producto.objects.get(id_producto = id_producto[i])
                detalleBoleta.id_boleta = boleta
                detalleBoleta.cantidad_detalleboleta = cantidad
                detalleBoleta.preciounitario_detalleboleta = precioUnitario
                detalleBoleta.subtotal_detalleboleta = subTotal
                detalleBoleta.save()
                totalVentas += subTotal
                producto = Producto.objects.get(id_producto = id_producto[i])
                producto.cant_stock_producto -= cantidad
                producto.save()
            boleta.total_ventas = totalVentas
            boleta.save()
            return redirect('generar_pdf', id_boleta = boleta.id_boleta)
        else:
            categorias= Categoria.objects.all()
            productos = Producto.objects.all()
            return render(request, 'procesoventa/procesoventa.html',{'categorias':categorias, 'productos':productos})
    except Exception as e:
        return HttpResponse("Error al obtener los datos de los usuarios- " + str(e))   
### PROCESOVENTA::END ###


@login_required()
def generar_pdf(request,id_boleta):
    boleta = Boleta.objects.get(id_boleta = id_boleta)
    productos = DetalleBoleta.objects.filter(id_boleta = id_boleta)
    template = get_template('boleta.html')
    context = {
        'nombre_cliente':boleta.nombrecliente_boleta.upper(),
        'fecha':boleta.fecha_boleta.strftime("%d/%m/%Y"),
        'total_venta':boleta.total_ventas,
        'productos':productos
    }
    html = template.render(context)
    string = html.encode(encoding="UTF-8")
    # tamaño de una boleta electronica
    pdf = HTML(string=string).write_pdf(stylesheets=[CSS(string='@page { size: 80mm 297mm; margin: 0mm; }')], presentational_hints=True)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="boleta.pdf"'
    return response

def reporte(request):
    try:
        if request.method == 'GET':
            ventas = Boleta.objects.all()
            return render(request,'reportes/reporte.html',{'ventas':ventas})
    except Exception as e:
        return HttpResponse("Error - " + str(e))