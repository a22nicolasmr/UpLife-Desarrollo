# # Usa una imagen base oficial de Python
# FROM python:3.11

# # Establece el directorio de trabajo dentro del contenedor
# WORKDIR /code

# # Copia el archivo de requisitos al contenedor
# COPY requirements.txt .
    
# # Instala las dependencias del proyecto
# RUN pip install --no-cache-dir -r requirements.txt

# # Copia el código del proyecto al directorio de trabajo en el contenedor
# COPY . /code/

# # Ejecuta el comando para crear un nuevo proyecto Django
# # RUN django-admin startproject password_generator .

# # Expone el puerto que Django usa por defecto
# EXPOSE 8000

# # Comando por defecto para ejecutar cuando se inicie el contenedor
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Usa unha imaxe de Python pequena
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Instala dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt

# Copia todo el código
COPY . .
RUN ls -l


# Asegura permisos de ejecución del entrypoint
RUN chmod +x entrypoint.sh

# Exponer el puerto (Render lo detectará automáticamente)
EXPOSE 8000

# Ejecuta el script de arranque
ENTRYPOINT ["./entrypoint.sh"]

