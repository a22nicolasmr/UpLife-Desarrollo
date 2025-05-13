# Usa una imagen base oficial de Python
FROM python:3.11

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /code

# Copia el archivo de requisitos al contenedor
COPY requirements.txt .
    
# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código del proyecto al directorio de trabajo en el contenedor
COPY . /code/

# Ejecuta el comando para crear un nuevo proyecto Django
# RUN django-admin startproject password_generator .

# Expone el puerto que Django usa por defecto
EXPOSE 8000

# Comando por defecto para ejecutar cuando se inicie el contenedor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# # Usa unha imaxe de Python pequena
# FROM python:3.11-slim

# # Establece directorio de traballo
# WORKDIR /app

# # Copia só o requirements.txt e instala dependencias primeiro (optimiza cache)
# COPY requirements.txt /app/
# RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt

# # Copia o resto do código
# COPY . /app/

# # Expón o porto 8000 (Render escoita neste porto)
# EXPOSE 8000

# # Recoller os ficheiros estáticos
# RUN python manage.py collectstatic --noinput

# # Comando que inicia o servidor de produción
# # CMD ["uvicorn", "UpLife.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--lifespan", "off"]
# # Cargar datos e logo iniciar o servidor
# CMD ["sh", "-c", "python manage.py migrate && python manage.py loaddata backup.json && uvicorn UpLife.asgi:application --host 0.0.0.0 --port 8000 --lifespan off"]

