# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de requisitos y los instala
COPY requirements.txt .

# Actualiza pip y instala las dependencias
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install python-dotenv

# Copia el resto del código de la aplicación
COPY . .

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
