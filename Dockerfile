FROM python:3.9-slim

WORKDIR /app

# Instalar dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copiar apenas o requirements.txt primeiro
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o resto dos arquivos
COPY . .

EXPOSE 5000

# Adicionar flags de debug
ENV PYTHONUNBUFFERED=1
ENV FLASK_DEBUG=1

# Usar python -u para output não-bufferizado
CMD ["python", "-u", "app.py"] 