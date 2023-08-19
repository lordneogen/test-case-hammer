FROM python:3.10.2

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y postgresql postgresql-contrib

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

ENV POSTGRES_DB=mydb
ENV POSTGRES_USER=myuser
ENV POSTGRES_PASSWORD=1234

RUN service postgresql start && \
    su - postgres -c "psql -c 'CREATE DATABASE $POSTGRES_DB;'" && \
    su - postgres -c "psql -c 'CREATE USER $POSTGRES_USER WITH PASSWORD '\''$POSTGRES_PASSWORD'\'';'" && \
    su - postgres -c "psql -c 'ALTER ROLE $POSTGRES_USER SET client_encoding TO '\''utf8'\'';'" && \
    su - postgres -c "psql -c 'ALTER ROLE $POSTGRES_USER SET default_transaction_isolation TO '\''read committed'\'';'" && \
    su - postgres -c "psql -c 'ALTER ROLE $POSTGRES_USER SET timezone TO '\''UTC'\'';'" && \
    su - postgres -c "psql -c 'GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_USER;'"

CMD ["python", "test_case/manage.py", "runserver", "0.0.0.0:8000"]
