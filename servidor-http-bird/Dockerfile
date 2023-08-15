# Utiliza la imagen base de Alpine Linux
FROM python:3.9-alpine

# Crea un usuario dentro del contenedor
RUN adduser -D myuser

# Define el directorio de trabajo
WORKDIR /app

# Cambia el propietario y permisos del directorio de trabajo
RUN chown myuser:myuser /app
RUN chmod -R 555 /app

# Cambia al usuario recién creado
USER myuser

# Expone el puerto 8003
EXPOSE 8003

# Ejecuta el servidor HTTP en el directorio de trabajo
CMD ["python", "-m", "http.server", "8003", "--bind", "0.0.0.0"]