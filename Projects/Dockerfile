FROM python:3.12-alpine

WORKDIR /app
RUN addgroup -S appgroup && adduser -S appuser -G appgroup 
USER appuser  
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app/* ./
EXPOSE 5000

CMD ["python", "main.py", "--host=0.0.0.0"]
