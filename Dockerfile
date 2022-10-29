FROM python:3.6.4

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r  requirements.txt

EXPOSE 8080
ENV PYTHONUNBUFFERED True

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
