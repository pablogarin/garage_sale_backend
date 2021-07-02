FROM python:3.8-slim-buster
ARG DB_FOLDER=/opt/api

WORKDIR /app

COPY ./api ./api
COPY ./requirements.txt ./requirements.txt
COPY ./gunicorn.config.py ./gunicorn.config.py
COPY ./jwt.key ./jwt.key
COPY ./jwt.key.pub ./jwt.key.pub

RUN python -m pip install -r requirements.txt
RUN mkdir ${DB_FOLDER}
RUN mkdir /app/uploads

EXPOSE 5016
ENV DB_PATH=${DB_FOLDER}/database.db
ENV PUBLIC_KEY=/app/jwt.key.pub
ENV PRIVATE_KEY=/app/jwt.key

CMD ["gunicorn", "-c", "gunicorn.config.py", "api.api:create_flask_app()"]