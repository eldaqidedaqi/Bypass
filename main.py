from flask import Blueprint, render_template, request, redirect, url_for
from app.services.abm_service import assign_device_to_mdm, get_abm_access_token
from app.services.gmail_service import check_activation_tickets, send_email

main_bp = Blueprint('main', __name__)

devices = [
    {"name": "iPhone 18.3", "serial": "FFWH7GJNN736", "status": "Desactivated"}
]

ticket_store = []

@main_bp.route('/')
def index():
    return render_template('main.html', devices=enumerate(devices), message=None)

@main_bp.route('/activate', methods=['POST'])
def activate():
    selected_idx = int(request.form['selected_device'])
    if request.form.get('terms') != 'accept':
        return render_template('main.html', devices=enumerate(devices), message="Debe aceptar los términos para continuar.")
    device = devices[selected_idx]
    try:
        token = get_abm_access_token()
        success, response = assign_device_to_mdm(token, device['serial'], '12345678-90ab-cdef-1234-567890abcdef')
        if success:
            device['status'] = 'Activated' if device['status'] == 'Desactivated' else 'Desactivated'
            message = f"Dispositivo {device['name']} ahora está {device['status']}."
            send_email(f"Dispositivo {device['serial']} actualizado", f"Estado cambiado a {device['status']}", 'eldaqidedaqi@gmail.com')
        else:
            message = f"Error asignando dispositivo: {response}"
    except Exception as e:
        message = f"Error: {str(e)}"
    return render_template('main.html', devices=enumerate(devices), message=message)

@main_bp.route('/tickets', methods=['GET'])
def tickets():
    global ticket_store
    try:
        ticket_store = check_activation_tickets()
    except Exception as e:
        ticket_store = []
        return f"Error al obtener tickets: {str(e)}"
    return render_template('tickets.html', tickets=ticket_store
