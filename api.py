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
def index():
    tasa_usd_clp = my_bcchapi.obtener_tasa_de_cambio()
    return render_template('index.html', tasa_usd_clp=tasa_usd_clp)

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

if __name__ == '__main__':
    app.run(debug=True)
