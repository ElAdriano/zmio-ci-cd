FROM python:3.9-slim

# Establish a working folder
WORKDIR /app

# Establish dependencies
COPY requirements.txt .
RUN python -m pip install -U pip wheel && \
    pip install -r requirements.txt

# Copy source files last because they change the most
COPY data_generator ./data_generator
COPY minmax ./minmax
COPY neural_network ./neural_network
COPY validators ./validators

COPY server.py .
COPY tests.py .
COPY wsgi.py .

# Run the service on port 8000
ENV PORT 8000
EXPOSE $PORT
CMD ["gunicorn", "wsgi:server", "--bind", "0.0.0.0:8000"]
