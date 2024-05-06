from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    port=3307,
    user="root",
    password="admin",
    database="Ferramas"
)

@app.route('/productos', methods=['POST'])
def add_producto():
    try:
        data = request.json
        print("Datos recibidos en POST:", data)  # Imprimir los datos recibidos en la consola del servidor Flask
    
        nombre = data.get('Nombre')
        descripcion = data.get('Descripcion')
        marca = data.get('Marca')
        modelo = data.get('Modelo')
        precio = data.get('Precio')
        stock = data.get('Stock')

        cursor = db.cursor()
        query = "INSERT INTO Productos (Nombre, Descripcion, Marca, Modelo, Precio, Stock) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (nombre, descripcion, marca, modelo, precio, stock))
        db.commit()
        cursor.close()
        
        return jsonify({"Mensaje": "Producto agregado correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/productos', methods=['GET'])
def get_productos():
    try:
        cursor = db.cursor()
        cursor.execute("SELECT CodigoProducto, Nombre, Descripcion, Marca, Modelo, Precio, Stock FROM Productos")
        productos = cursor.fetchall()
        cursor.close()
        
        # Formatear los resultados en un formato JSON
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

@app.route('/productos/<codigo_producto>', methods=['PUT'])
def update_producto(codigo_producto):
    try:
        data = request.json
        print("Datos recibidos en PUT:", data)  # Imprimir los datos recibidos en la consola del servidor Flask
    
        nombre = data.get('Nombre')
        descripcion = data.get('Descripcion')
        marca = data.get('Marca')
        modelo = data.get('Modelo')
        precio = data.get('Precio')
        stock = data.get('Stock')

        cursor = db.cursor()
        query = "UPDATE Productos SET Nombre = %s, Descripcion = %s, Marca = %s, Modelo = %s, Precio = %s, Stock = %s WHERE CodigoProducto = %s"
        cursor.execute(query, (nombre, descripcion, marca, modelo, precio, stock, codigo_producto))
        db.commit()
        cursor.close()
        
        return jsonify({"Mensaje": "Producto actualizado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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

if __name__ == '__main__':
    app.run(debug=True)
