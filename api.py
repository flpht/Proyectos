from webpay_plus_config import transaction
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.options import WebpayOptions
from transbank.common.integration_type import IntegrationType
from transbank.common.integration_commerce_codes import IntegrationCommerceCodes
from transbank.common.integration_api_keys import IntegrationApiKeys
from flask import Flask, render_template, request, jsonify
import mysql.connector
import uuid
import my_bcchapi

app = Flask(__name__)


# Configuración de la base de datos
db = mysql.connector.connect(
    host="localhost",
    port=3307,
    user="root",
    password="Noel123456",
    database="Ferramas"
)

# Ruta para la página de inicio
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/inicio')
def productos():
    return render_template('inicio.html')


@app.route('/conversor')
def conversor():
    tasa_usd_clp = my_bcchapi.obtener_tasa_de_cambio()
    return render_template('conversor_moneda.html', tasa_usd_clp=tasa_usd_clp)


# Ruta para agregar un producto
@app.route('/productos', methods=['POST'])
def add_producto():
    try:
        data = request.json
        print("Datos recibidos en POST:", data)  
    
        nombre = data.get('Nombre')
        descripcion = data.get('Descripcion')
        marca = data.get('Marca')
        modelo = data.get('Modelo')
        precio = data.get('Precio')
        stock = data.get('Stock')
        
        codigo_producto = "FER-" + str(uuid.uuid4().hex)[:8]

        cursor = db.cursor()
        query = "INSERT INTO Productos (CodigoProducto, Nombre, Descripcion, Marca, Modelo, Precio, Stock) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (codigo_producto, nombre, descripcion, marca, modelo, precio, stock))
        db.commit()
        cursor.close()
        
        return jsonify({"Mensaje": "Producto agregado correctamente", "CodigoProducto": codigo_producto}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para obtener todos los productos
@app.route('/productos', methods=['GET'])
def get_productos():
    try:
        cursor = db.cursor()
        cursor.execute("SELECT CodigoProducto, Nombre, Descripcion, Marca, Modelo, Precio, Stock FROM Productos")
        productos = cursor.fetchall()
        cursor.close()
        
        productos_json = []
        for producto in productos:
            producto_json = {
                "CodigoProducto": producto[0],
                "Nombre": producto[1],
                "Descripcion": producto[2],
                "Marca": producto[3],
                "Modelo": producto[4],
                "Precio": producto[5],
                "Stock": producto[6]
            }
            productos_json.append(producto_json)
        
        return jsonify(productos_json), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para eliminar un producto por su código
@app.route('/productos/<codigo_producto>', methods=['DELETE'])
def delete_producto(codigo_producto):
    try:
        cursor = db.cursor()
        query = "DELETE FROM Productos WHERE CodigoProducto = %s"
        cursor.execute(query, (codigo_producto,))
        db.commit()
        cursor.close()
        
        return jsonify({"Mensaje": "Producto eliminado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para convertir moneda
@app.route('/convertir', methods=['POST'])

def convertir():
    try:
        datos = request.get_json()
        monto = float(datos['monto'])
        moneda = datos['moneda']
        tasa_usd_clp = my_bcchapi.obtener_tasa_de_cambio()
        if tasa_usd_clp:
            resultado = my_bcchapi.convertir_moneda(monto, moneda, tasa_usd_clp)
            return jsonify({'resultado': resultado})
        else:
            return jsonify({'error': 'No se pudo obtener la tasa de cambio'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/iniciar_pago', methods=['POST'])
def iniciar_pago():

    try:
        buy_order = request.form['buy_order']
        session_id = request.form['session_id']
        amount = float(request.form['amount'])
        return_url = request.form['return_url']

        response = transaction.create(buy_order, session_id, amount, return_url)
        token = response['token']
        payment_url = response['url']

        return render_template('payment_form.html', payment_url=payment_url, token=token)
    
    except Exception as e:
        print("Error al crear la transacción:", str(e))
        error_message = 'Ocurrió un error al crear la transacción. Por favor, intenta nuevamente.'
        return render_template('error.html', error_message=error_message)
    

@app.route('/confirmacion', methods=['GET', 'POST'])
def confirmacion():
    print("Llegada a la función confirmacion()")
    print("Método de la solicitud:", request.method)

    if request.method == 'POST':
        token = request.form.get('token_ws')
    else:
        token = request.args.get('token_ws')

    print("Token recibido:", token)

    if token:
        try:
            # Configurar las opciones de Webpay
            webpay_options = WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST)

            # Crear una instancia de la transacción con las opciones de Webpay
            transaction = Transaction(webpay_options)

            print("Confirmando la transacción...")

            # Confirmar la transacción
            response = transaction.commit(token)

            print("Respuesta de la confirmación:", response)

            if response['response_code'] == 0:
                # La transacción fue confirmada exitosamente
                print("La transacción fue confirmada exitosamente")
                return render_template('confirmacion.html', response=response)
            else:
                # La transacción no fue confirmada
                print("La transacción no fue confirmada")
                error_message = 'La transacción no pudo ser confirmada. Por favor, intenta nuevamente.'
                return render_template('error.html', error_message=error_message)
        except Exception as e:
            print("Error al confirmar la transacción:")
            print(str(e))
            import traceback
            traceback.print_exc()
            error_message = 'Ocurrió un error al procesar la transacción. Por favor, intenta nuevamente.'
            return render_template('error.html', error_message=error_message)
    else:
        # El token no fue recibido
        print("Token no proporcionado o inválido")
        error_message = 'Token no proporcionado o inválido.'
        return render_template('error.html', error_message=error_message)


@app.route('/retorno', methods=['GET', 'POST'])
def retorno():
    if request.method == 'POST':
        token_ws = request.form.get('token_ws')
    else:
        token_ws = request.args.get('token_ws')

    return confirmacion(token_ws)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
