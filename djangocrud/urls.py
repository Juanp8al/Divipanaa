"""
URL configuration for djangocrud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include('allauth.urls')),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'), 
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks/complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('tasks/delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('gastos/eliminar-todos/', views.eliminar_todos_gastos_usuario, name='eliminar_todos_gastos_usuario'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('gasto/crear/', views.crear_gasto, name='crear_gasto'),
    path('liquidar/', views.liquidar_deudas, name='liquidar_deudas'),
    path('amigos/', views.amigos, name='amigos'),
    path('gasto/eliminar/<int:gasto_id>/', views.eliminar_gasto, name='eliminar_gasto'),
    path('actividad-reciente/', views.actividad_reciente, name='actividad_reciente'),
    path('todos_gastos/', views.todos_los_gastos, name='todos_gastos'),



]
