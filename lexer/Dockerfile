FROM python:3.12-slim
WORKDIR /app
# Install deps
COPY lexer/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
# Copy service and core module it wraps
COPY lexer/service.py /app/service.py
COPY lexer.py /app/lexer.py
EXPOSE 5001
CMD ["uvicorn", "service:app", "--host", "0.0.0.0", "--port", "5001"]
