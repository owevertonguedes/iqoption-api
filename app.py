from flask import Flask, request, jsonify
import logging
import sys
from iqoptionapi.stable_api import IQ_Option

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logging.getLogger('iqoptionapi.ws.client').setLevel(logging.INFO)
logging.getLogger('iqoptionapi').setLevel(logging.INFO)
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
        balance_mode = data.get('balance_mode', 'PRACTICE')  # Padrão é PRACTICE

        logger.info(f"Tentando conectar com email: {email} - Modo: {balance_mode}")
        
        # Validar modo de conta
        if balance_mode not in ['PRACTICE', 'REAL']:
            return jsonify({
                "status": "error",
                "message": "Modo de balance inválido. Use 'PRACTICE' ou 'REAL'",
                "details": {
                    "balance_mode": balance_mode
                }
            }), 400

        iq = IQ_Option(email, password)
        status, reason = iq.connect()

        if not status:
            logger.error(f"Falha na conexão: {reason}")
            return jsonify({"status": "error", "message": reason}), 401

        # Mudar para o modo de conta especificado
        iq.change_balance(balance_mode)
        logger.info(f"Conta alterada para {balance_mode}")

        # Verificar se a mudança foi bem sucedida
        current_balance = iq.get_balance_mode()
        if current_balance != balance_mode:
            logger.error(f"Falha ao alterar para modo {balance_mode}. Balance atual: {current_balance}")
            return jsonify({
                "status": "error",
                "message": f"Não foi possível mudar para modo {balance_mode}",
                "details": {
                    "requested_mode": balance_mode,
                    "current_mode": current_balance
                }
            }), 400

        balance = iq.get_balance()
        logger.info(f"Conexão bem sucedida. Saldo: {balance} - Modo: {balance_mode}")
        return jsonify({
            "status": "success",
            "connected": True,
            "balance": balance,
            "balance_mode": balance_mode
        })
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

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
        balance_mode = data.get('balance_mode', 'PRACTICE')  # Padrão é PRACTICE

        logger.info(f"Tentando operação: {asset}, {direction}, {amount}, {duration} - Modo: {balance_mode}")

        # Validar modo de conta
        if balance_mode not in ['PRACTICE', 'REAL']:
            return jsonify({
                "status": "error",
                "message": "Modo de balance inválido. Use 'PRACTICE' ou 'REAL'",
                "details": {
                    "balance_mode": balance_mode
                }
            }), 400

        iq = IQ_Option(email, password)
        status, reason = iq.connect()

        if not status:
            logger.error(f"Falha na conexão: {reason}")
            return jsonify({"status": "error", "message": "Falha na conexão"}), 401

        # Mudar para o modo de conta especificado
        iq.change_balance(balance_mode)
        logger.info(f"Conta alterada para {balance_mode}")

        # Verificar se a mudança foi bem sucedida
        current_balance = iq.get_balance_mode()
        if current_balance != balance_mode:
            logger.error(f"Falha ao alterar para modo {balance_mode}. Balance atual: {current_balance}")
            return jsonify({
                "status": "error",
                "message": f"Não foi possível mudar para modo {balance_mode}",
                "details": {
                    "requested_mode": balance_mode,
                    "current_mode": current_balance
                }
            }), 400

        status, id = iq.buy(amount, asset, direction, duration)

        if status:
            logger.info(f"Ordem executada com sucesso. ID: {id} - Modo: {balance_mode}")
            return jsonify({
                "status": "success",
                "order_id": id,
                "balance_mode": balance_mode
            })
        else:
            logger.error("Falha ao executar ordem")
            return jsonify({
                "status": "error",
                "message": "Falha ao executar ordem",
                "details": {
                    "balance_mode": balance_mode,
                    "asset": asset,
                    "amount": amount,
                    "direction": direction,
                    "duration": duration
                }
            }), 400
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

        logger.info(f"Tentando operação: {asset}, {direction}, {amount}, {duration}")

        iq = IQ_Option(email, password)
        status, reason = iq.connect()

        if not status:
            logger.error(f"Falha na conexão: {reason}")
            return jsonify({"status": "error", "message": "Falha na conexão"}), 401

        # Garantir que a conta esteja em modo PRACTICE
        iq.change_balance('PRACTICE')
        logger.info("Conta alterada para PRACTICE")

        # Verificar se está em modo PRACTICE
        current_balance = iq.get_balance_mode()
        if current_balance != 'PRACTICE':
            logger.error(f"Falha ao alterar para modo PRACTICE. Balance atual: {current_balance}")
            return jsonify({
                "status": "error",
                "message": "Não foi possível mudar para modo demo",
                "details": {
                    "current_balance": current_balance
                }
            }), 400

        status, id = iq.buy(amount, asset, direction, duration)

        if status:
            logger.info(f"Ordem executada com sucesso. ID: {id}")
            return jsonify({
                "status": "success",
                "order_id": id
            })
        else:
            logger.error("Falha ao executar ordem")
            return jsonify({
                "status": "error",
                "message": "Falha ao executar ordem",
                "details": {
                    "balance_mode": current_balance,
                    "asset": asset,
                    "amount": amount,
                    "direction": direction,
                    "duration": duration
                }
            }), 400
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    logger.info("Iniciando servidor Flask...")
    app.run(host='0.0.0.0', port=5000, debug=True) 