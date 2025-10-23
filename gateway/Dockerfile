FROM python:3.12-slim
WORKDIR /app
COPY gateway/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY gateway/service.py /app/service.py
EXPOSE 5000
COPY gateway/wait_and_run.py /app/wait_and_run.py
CMD ["python", "/app/wait_and_run.py"]
