FROM python:3.10-slim

# Установка зависимостей
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Установка gunicorn, если нет в requirements.txt
RUN pip install gunicorn

# Копируем проект
COPY . .

# Собираем статику, если нужно
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "gamehub.wsgi:application", "--bind", "0.0.0.0:8000"]
