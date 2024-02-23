FROM python:3.10-slim
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY . .

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi"]