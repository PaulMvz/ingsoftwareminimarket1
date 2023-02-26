from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre_usuario = models.CharField(max_length=30, null=True)
    apellidos_usuarios = models.CharField(max_length=50, null=True)
    usuario = models.ForeignKey(User, models.DO_NOTHING, db_column='usuario', blank=True, null=True)

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=40, null=True)
    imagen_categoria = models.ImageField(upload_to='Categorias', blank=True, null=True)

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    codigo_producto = models.CharField(max_length=30, null=True)
    nombre_producto = models.CharField(max_length=25, null=True)
    descripcion_producto = models.CharField(max_length=150, null=True)
    cant_stock_producto = models.IntegerField(null=True)
    imagen_producto = models.ImageField(upload_to='Productos', blank=True, null=True)
    precio_producto = models.DecimalField(max_digits=5, decimal_places=2, null=True)

class Boleta(models.Model):
    id_boleta = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombrecliente_boleta = models.CharField(max_length=60, null=True)
    total_ventas = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    fecha_boleta = models.DateField(null=True)

class DetalleBoleta(models.Model):
    id_detalleboleta = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    id_boleta = models.ForeignKey(Boleta, on_delete=models.CASCADE)
    cantidad_detalleboleta = models.IntegerField(null=True)
    preciounitario_detalleboleta = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    subtotal_detalleboleta = models.DecimalField(max_digits=10, decimal_places=2, null=True)


# Create your models here.
