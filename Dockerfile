FROM python:3.11-slim

# Evitem que Python generi fitxers brossa
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

# Instal·lem Django i el connector de Postgres directament
# Fem servir psycopg2-binary per evitar haver d'instal·lar gcc (l'error d'abans)
RUN pip install django psycopg2-binary

COPY . /code/