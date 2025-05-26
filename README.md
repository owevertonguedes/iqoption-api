# API IQ Option Service

API REST para integração com a IQ Option, permitindo conexão e execução de operações via HTTP.

## Endpoints

### POST /api/connect
Conecta à conta IQ Option.

**Request Body:**
```json
{
    "email": "seu_email",
    "password": "sua_senha"
}
```

**Response:**
```json
{
    "status": "success",
    "connected": true,
    "balance": 1000.00
}
```

### POST /api/trade
Executa uma operação na IQ Option.

**Request Body:**
```json
{
    "email": "seu_email",
    "password": "sua_senha",
    "asset": "EURUSD",
    "amount": 1,
    "direction": "call",
    "duration": 1
}
```

**Response:**
```json
{
    "status": "success",
    "order_id": "123456"
}
```

## Instalação

1. Clone o repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```
3. Execute a aplicação:
```bash
python app.py
```

## Docker

Para executar com Docker:
```bash
docker build -t iqoption-api .
docker run -p 5000:5000 iqoption-api
```

## Notas

- A API usa conta de demonstração (PRACTICE)
- Por padrão, opera com EURUSD
- Duração padrão é 1 minuto
- Valores padrão: amount=1, direction=call 