FROM python:3.12

WORKDIR /app

RUN pip install gunicorn

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /app/initial_scripts.sh
ENTRYPOINT ["/app/initial_scripts.sh"]

CMD ["gunicorn", "-b", "0.0.0.0:8000", "backend.wsgi"]