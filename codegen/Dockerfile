FROM python:3.12-slim
WORKDIR /app
COPY codegen/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY codegen/service.py /app/service.py
COPY codegen.py /app/codegen.py
# folder for output; compose will mount a volume here
RUN mkdir -p /output
EXPOSE 5003
CMD ["uvicorn", "service:app", "--host", "0.0.0.0", "--port", "5003"]
