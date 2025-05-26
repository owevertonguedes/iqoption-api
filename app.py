from flask import Flask, request, jsonify
import logging
import sys
from iqoptionapi.stable_api import IQ_Option

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200

@app.route('/api/connect', methods=['POST'])
def connect():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        logger.info(f"Tentando conectar com email: {email}")
        
        iq = IQ_Option(email, password)
        status, reason = iq.connect()

        if status:
            balance = iq.get_balance()
            logger.info(f"Conexão bem sucedida. Saldo: {balance}")
            return jsonify({
                "status": "success",
                "connected": True,
                "balance": balance
            })
        else:
            logger.error(f"Falha na conexão: {reason}")
            return jsonify({"status": "error", "message": reason}), 401
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/trade', methods=['POST'])
def trade():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        asset = data.get('asset', 'EURUSD')
        amount = data.get('amount', 1)
        direction = data.get('direction', 'call')
        duration = data.get('duration', 1)

        logger.info(f"Tentando operação: {asset}, {direction}, {amount}, {duration}")

        iq = IQ_Option(email, password)
        status, reason = iq.connect()

        if not status:
            logger.error(f"Falha na conexão: {reason}")
            return jsonify({"status": "error", "message": "Falha na conexão"}), 401

        iq.change_balance('PRACTICE')
        logger.info("Conta alterada para PRACTICE")

        status, id = iq.buy(amount, asset, direction, duration)

        if status:
            logger.info(f"Ordem executada com sucesso. ID: {id}")
            return jsonify({
                "status": "success",
                "order_id": id
            })
        else:
            logger.error("Falha ao executar ordem")
            return jsonify({"status": "error", "message": "Falha ao executar ordem"}), 400
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    logger.info("Iniciando servidor Flask...")
    app.run(host='0.0.0.0', port=5000, debug=True) 