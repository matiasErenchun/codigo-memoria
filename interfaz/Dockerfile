# etapa de compilación
FROM node:18.17.0-alpine as build-stage
# hacer la carpeta 'app' el directorio de trabajo actual
WORKDIR /app
# copiar 'package.json' y 'package-lock.json' (si están disponibles)
COPY interfazraptordetector/package*.json ./
# instalar dependencias del proyecto
RUN npm install --openssl-legacy-provider
# copiar los archivos y carpetas del proyecto al directorio de trabajo actual (es decir, la carpeta 'app')
COPY interfazraptordetector .
# construir aplicación para producción minificada
RUN export NODE_OPTIONS=--openssl-legacy-provider && npm run build

# etapa de producción
FROM nginx:1.24.0-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]