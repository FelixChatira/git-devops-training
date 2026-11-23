
FROM python:3.12-slim

WORKDIR /app

COPY app/requirements.txt .
COPY wheelhouse/ /wheelhouse/

RUN pip install \
    --no-index \
    --find-links=/wheelhouse \
    --no-cache-dir \
    -r requirements.txt

COPY app/ .

EXPOSE 5000

CMD ["sh", "-c", "python -c 'from web import initialize_database; initialize_database()' && gunicorn --bind 0.0.0.0:5000 web:app"]

