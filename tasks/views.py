from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_backends
from django.utils import timezone
from django.db import models
from django.views.decorators.http import require_POST
from django.contrib import messages
# Importar modelos personalizados
from .models import (
    Usuario, 
    Sesion, 
    Gasto, 
    Participante, 
    Task,
    DetalleGasto
)

def home(request):
    return render(request, 'home.html')

def signup(request): # type: ignore
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], 
                    password=request.POST['password1']
                )

                backend = get_backends()[0]
                user.backend = f"{backend.__module__}.{backend.__class__.__name__}"
                
                login(request, user)
                return redirect('home')

            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm(),
                    "error": 'Nombre de usuario ya existente'
                })

        return render(request, 'signup.html', {
            'form': UserCreationForm(),
            "error": 'Las contraseñas no coinciden'
        })

@login_required
def crear_sesion(request):
    if request.method == 'POST':
        usuario = Usuario.objects.get(nombre=request.user.username)
        sesion = Sesion.objects.create(
            estado='activa', 
            modo_propina='manual'
        )
        Participante.objects.create(
            usuario=usuario,
            sesion=sesion
        )
        return redirect('detalle_sesion', sesion_id=sesion.id)
    
    return render(request, 'crear_sesion.html')

@login_required
def detalle_sesion(request, sesion_id):
    sesion = get_object_or_404(Sesion, id=sesion_id)
    gastos = Gasto.objects.filter(sesion=sesion)
    participantes = Participante.objects.filter(sesion=sesion)
    
    return render(request, 'detalle_sesion.html', {
        'sesion': sesion,
        'gastos': gastos,
        'participantes': participantes
    })
@login_required
def agregar_gasto(request, sesion_id):
    sesion = get_object_or_404(Sesion, id=sesion_id)

    if request.method == 'POST':
        usuario = Usuario.objects.get(nombre=request.user.username)

        Gasto.objects.create(
            sesion=sesion,
            usuario=usuario,
            descripcion=request.POST.get('descripcion'),
            monto=request.POST.get('monto')
        )

        messages.success(request, '✅ ¡Gasto agregado correctamente!')
        return redirect('tasks')  # Asegúrate que esta vista carga el template donde están los mensajes

    return render(request, 'agregar_gasto.html', {'sesion': sesion})


def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, 
            username=request.POST['username'], 
            password=request.POST['password']
        )
        if user is None: 
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'El usuario o la contraseña son incorrectos'
            }) 
        else: 
            login(request, user)
            return redirect('tasks')

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user)
    pending_tasks = tasks.filter(date_completed__isnull=True)
    completed_tasks = tasks.filter(date_completed__isnull=False)
    
    if request.method == 'POST':
        try:
            Task.objects.create(
                title=request.POST.get('title'),
                description=request.POST.get('description', ''),
                important=request.POST.get('important') == 'on',
                user=request.user
            )
            return redirect('tasks')
        except Exception as e:
            return render(request, 'tasks.html', {
                'pending_tasks': pending_tasks,
                'completed_tasks': completed_tasks,
                'error': str(e)
            })
    
    return render(request, 'tasks.html', {
        'pending_tasks': pending_tasks,
        'completed_tasks': completed_tasks,
        'completed_tasks_count': completed_tasks.count()
    })

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.date_completed = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

# ✅ FUNCIÓN CON CORRECCIÓN: se asegura que el Usuario exista
@login_required
@login_required
def dashboard(request):
    try:
        usuario = Usuario.objects.get(user=request.user)
    except Usuario.DoesNotExist:
        usuario_existente = Usuario.objects.filter(email=request.user.email).first()
        if usuario_existente:
            if usuario_existente.user is None:
                usuario_existente.user = request.user
                usuario_existente.save()
            usuario = usuario_existente
        else:
            usuario = Usuario.objects.create(
                user=request.user,
                nombre=request.user.username,
                email=request.user.email or '',
                contrasena='temporal'
            )

    tasks = Task.objects.filter(user=request.user)
    gastos = Gasto.objects.filter(usuario=usuario).order_by('-fecha')

    total_gastos = gastos.aggregate(models.Sum('monto'))['monto__sum'] or 0

    participaciones = Participante.objects.filter(usuario=usuario)

    return render(request, 'tasks.html', {
        'usuario': usuario,
        'tasks': tasks,
        'gastos': gastos,
        'total_gastos': total_gastos,
        'participaciones': participaciones
    })



@login_required
def crear_gasto(request):
    if request.method == 'POST':
        descripcion = request.POST.get('descripcion')
        monto_total = float(request.POST.get('monto'))

        # === Obtener o crear el Usuario asociado ===
        try:
            # Buscar si ya existe un Usuario asociado al User
            usuario = Usuario.objects.get(user=request.user)
        except Usuario.DoesNotExist:
            # Buscar si existe un Usuario con el mismo email
            usuario_existente = Usuario.objects.filter(email=request.user.email).first()
            if usuario_existente:
                # Si ya existe, lo vinculamos al User actual (si aún no lo está)
                if usuario_existente.user is None:
                    usuario_existente.user = request.user
                    usuario_existente.save()
                usuario = usuario_existente
            else:
                # Crear uno nuevo solo si no existe ninguno con ese email
                usuario = Usuario.objects.create(
                    user=request.user,
                    nombre=request.user.username,
                    email=request.user.email or '',
                    contrasena='temporal'  # Cambia esto si usas un sistema real de contraseñas
                )

        # === Crear el gasto principal ===
        gasto = Gasto.objects.create(
            usuario=usuario,
            descripcion=descripcion,
            monto=monto_total
        )

        # === Buscar sesión activa ===
        sesiones_activas = Sesion.objects.filter(
            estado='activa',
            participante__usuario=usuario
        )

        if sesiones_activas.exists():
            sesion = sesiones_activas.first()
            gasto.sesion = sesion
            gasto.save()

            participantes = Participante.objects.filter(sesion=sesion)
            cantidad_participantes = participantes.count()

            if cantidad_participantes > 0:
                monto_individual = monto_total / cantidad_participantes

                for participante in participantes:
                    DetalleGasto.objects.create(
                        gasto=gasto,
                        participante=participante,
                        contribucion=monto_individual
                    )

                    # Si no es quien pagó, sumamos a su deuda
                    if participante.usuario != usuario:
                        if participante.monto_a_pagar is None:
                            participante.monto_a_pagar = monto_individual
                        else:
                            participante.monto_a_pagar += monto_individual
                        participante.save()

        return redirect('dashboard')

    # Si es GET, mostrar el formulario
    return render(request, 'crear_gasto.html')
@login_required
def liquidar_deudas(request):
   
    # Aquí iría lógica real de cálculo (pendiente)
    return render(request, 'liquidar.html', {
        
    })

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], 
                    password=request.POST['password1']
                )

                backend = get_backends()[0]  # Obtener el backend configurado
                user.backend = f"{backend.__module__}.{backend.__class__.__name__}"
                
                login(request, user)
                return redirect('home')  # ⬅️ Redirige a 'home' en lugar de 'sesiones'

            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'Nombre de usuario ya existente'
                })

        return render(request, 'signup.html', {
            'form': UserCreationForm,
            "error": 'Las contraseñas no coinciden'
        })


@login_required
def amigos(request):
    return render(request, 'amigos.html')

from django.http import JsonResponse

def eliminar_gasto(request, gasto_id):
    gasto = get_object_or_404(Gasto, id=gasto_id)
    if request.method == 'POST':
        gasto.delete()
        return JsonResponse({'ok': True})
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@require_POST
@login_required
@require_POST
@login_required
def eliminar_todos_gastos_usuario(request):
    # Asegura que el usuario de Django tenga su objeto Usuario asociado
    try:
        usuario = Usuario.objects.get(user=request.user)
    except Usuario.DoesNotExist:
        usuario_existente = Usuario.objects.filter(email=request.user.email).first()
        if usuario_existente:
            if usuario_existente.user is None:
                usuario_existente.user = request.user
                usuario_existente.save()
            usuario = usuario_existente
        else:
            usuario = Usuario.objects.create(
                user=request.user,
                nombre=request.user.username,
                email=request.user.email or '',
                contrasena='temporal'
            )

    # Eliminar sus gastos
    Gasto.objects.filter(usuario=usuario).delete()

    return redirect('dashboard')

@login_required
def actividad_reciente(request):
    # Obtener o crear el Usuario asociado al User
    try:
        usuario = Usuario.objects.get(user=request.user)
    except Usuario.DoesNotExist:
        usuario_existente = Usuario.objects.filter(email=request.user.email).first()
        if usuario_existente:
            if usuario_existente.user is None:
                usuario_existente.user = request.user
                usuario_existente.save()
            usuario = usuario_existente
        else:
            usuario = Usuario.objects.create(
                user=request.user,
                nombre=request.user.username,
                email=request.user.email or '',
                contrasena='temporal'
            )

    # Obtener los últimos 10 gastos del usuario
    gastos = Gasto.objects.filter(usuario=usuario).order_by('-fecha')[:10]

    return render(request, 'actividad_reciente.html', {'gastos': gastos})

@login_required
def todos_los_gastos(request):
    # Obtener o crear el Usuario asociado al User
    try:
        usuario = Usuario.objects.get(user=request.user)
    except Usuario.DoesNotExist:
        usuario_existente = Usuario.objects.filter(email=request.user.email).first()
        if usuario_existente:
            if usuario_existente.user is None:
                usuario_existente.user = request.user
                usuario_existente.save()
            usuario = usuario_existente
        else:
            usuario = Usuario.objects.create(
                user=request.user,
                nombre=request.user.username,
                email=request.user.email or '',
                contrasena='temporal'
            )

    # Obtener todos los gastos del usuario
    gastos = Gasto.objects.filter(usuario=usuario)

    return render(request, 'todos_gastos.html', {'gastos': gastos})
