# API IQ Option Service

API REST para integração com a IQ Option, permitindo conexão e execução de operações via HTTP.

## Endpoints

### POST /api/connect
Conecta à conta IQ Option.

**Request Body:**
```json
{
    "email": "seu_email",
    "password": "sua_senha",
    "balance_mode": "PRACTICE"  // Pode ser "PRACTICE" ou "REAL"
}
```

**Response:**
```json
{
    "status": "success",
    "connected": true,
    "balance": 1000.00,
    "balance_mode": "PRACTICE"
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
    "duration": 1,
    "balance_mode": "PRACTICE"  // Pode ser "PRACTICE" ou "REAL"
}
```

**Response:**
```json
{
    "status": "success",
    "order_id": "123456",
    "balance_mode": "PRACTICE"
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

- O parâmetro `balance_mode` é opcional e pode ser "PRACTICE" ou "REAL"
- Se não especificado, o padrão é "PRACTICE"
- Por padrão, opera com EURUSD
- Duração padrão é 1 minuto
- Valores padrão: amount=1, direction=call
- A API retorna logs detalhados em caso de erro, incluindo o modo de conta usado