from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} by {self.user.username}"


class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre


class Sesion(models.Model):
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=50)  # 'activa' o 'cerrada'
    total_gasto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_propina = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    modo_propina = models.CharField(max_length=50)  # 'manual' o 'ruleta'

    def __str__(self):
        return f"Sesion {self.id} - {self.fecha_inicio}" # type: ignore


class Participante(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    sesion = models.ForeignKey(Sesion, on_delete=models.CASCADE)
    monto_a_pagar = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('usuario', 'sesion')

    def __str__(self):
        return f"{self.usuario.nombre} en {self.sesion}"


class Gasto(models.Model):
    sesion = models.ForeignKey(Sesion, on_delete=models.SET_NULL, null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=255)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.descripcion} - {self.monto}"


class DetalleGasto(models.Model):
    gasto = models.ForeignKey(Gasto, on_delete=models.CASCADE)
    participante = models.ForeignKey(Participante, on_delete=models.PROTECT)
    contribucion = models.DecimalField(max_digits=10, decimal_places=2)


class Propina(models.Model):
    sesion = models.OneToOneField(Sesion, on_delete=models.CASCADE)  # ← corrección aquí
    participante = models.ForeignKey(Participante, on_delete=models.PROTECT)
    monto_propina = models.DecimalField(max_digits=10, decimal_places=2)


class Auditoria(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    accion = models.CharField(max_length=50)  # 'creacion', 'modificacion', 'eliminacion'
    fecha_hora = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=255, null=True, blank=True)
