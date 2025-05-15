#!/usr/bin/env bash
# Exit on error
set -o errexit

# Instala las dependencias
pip install -r requirements.txt

# Recolecta archivos estáticos
python manage.py collectstatic --no-input

# Aplica migraciones
python manage.py migrate
