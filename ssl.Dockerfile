FROM python:3.11.1

COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade wheel
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app /app
COPY ./openssl.cnf /openssl.cnf
COPY ./logging.yaml /logging.yaml

EXPOSE 8000
ENV OPENSSL_CONF="./openssl.cnf"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-config", "logging.yaml"]
