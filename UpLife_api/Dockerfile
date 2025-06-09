# Usa unha imaxe de Python pequena
FROM python:3.11-slim

# Directorio de traballo
WORKDIR /app

# Instala dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt

# Copia todo o código
COPY . .
RUN ls -l


# Asegura permisos de execución do entrypoint
RUN chmod +x entrypoint.sh

# Exponer o puerto 
EXPOSE 8000

# Executa  script de arranque
ENTRYPOINT ["./entrypoint.sh"]

