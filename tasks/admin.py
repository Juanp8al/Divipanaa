from django.contrib import admin
from django.urls import path, include
from .models import (
    Usuario, 
    Sesion, 
    Participante, 
    Gasto, 
    DetalleGasto, 
    Propina, 
    Auditoria,
    Task  # Mantengo Task si aún lo necesitas
)

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email')
    search_fields = ('nombre', 'email')

class SesionAdmin(admin.ModelAdmin):
    list_display = ('fecha_inicio', 'fecha_fin', 'estado', 'total_gasto', 'modo_propina')
    list_filter = ('estado', 'modo_propina')

class ParticipanteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'sesion', 'monto_a_pagar')
    list_filter = ('sesion',)

class GastoAdmin(admin.ModelAdmin):
    list_display = ('sesion', 'usuario', 'descripcion', 'monto', 'fecha')
    list_filter = ('sesion', 'fecha')
    search_fields = ('descripcion',)

class DetalleGastoAdmin(admin.ModelAdmin):
    list_display = ('gasto', 'participante', 'contribucion')
    list_filter = ('gasto', 'participante')

class PropinaAdmin(admin.ModelAdmin):
    list_display = ('sesion', 'participante', 'monto_propina')

class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'accion', 'fecha_hora')
    list_filter = ('accion', 'fecha_hora')

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'date_completed', 'important')
    list_filter = ('important', 'date_completed')


# Registrar todos los modelos con sus respectivas configuraciones de admin
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Sesion, SesionAdmin)
admin.site.register(Participante, ParticipanteAdmin)
admin.site.register(Gasto, GastoAdmin)
admin.site.register(DetalleGasto, DetalleGastoAdmin)
admin.site.register(Propina, PropinaAdmin)
admin.site.register(Auditoria, AuditoriaAdmin)
admin.site.register(Task, TaskAdmin)