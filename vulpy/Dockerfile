FROM python:3.11-slim

WORKDIR /app

# Installation des dependances
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .

# Argument pour choisir le répertoire (bad ou good)
ARG APP_DIR=bad

# Initialisation de la base de donnees
WORKDIR /app/${APP_DIR}
RUN python db_init.py || true

# Modifier le fichier Python pour écouter sur 0.0.0.0:5000
RUN sed -i "s/host='127.0.1.1'/host='0.0.0.0'/g" vulpy.py && \
    sed -i "s/port=5001/port=5000/g" vulpy.py

EXPOSE 5000

CMD ["python", "vulpy.py"]
