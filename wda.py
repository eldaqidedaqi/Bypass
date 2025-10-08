from flask import Blueprint, jsonify, render_template, request
from app.services.wda_service import wda

wda_bp = Blueprint('wda', __name__, url_prefix='/wda')

@wda_bp.route('/')
def control():
    return render_template('wda.html')

@wda_bp.route('/status')
def status():
    try:
        status = wda.status()
        return jsonify({"status": status})
    except Exception as e:
        return jsonify({"error": str(e)})

@wda_bp.route('/home', methods=['POST'])
def home():
    try:
        wda.home()
        return jsonify({"result": "Botón Home presionado"})
    except Exception as e:
        return jsonify({"error": str(e)})

@wda_bp.route('/activate', methods=['POST'])
def activate():
    try:
        # Acciones adicionales para activar dispositivo si se desean colocar aquí
        return jsonify({"result": "Activación simulada realizada"})
    except Exception as e:
        return jsonify({"error": str(e)})
