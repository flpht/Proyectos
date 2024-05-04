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

@app.route('/productos', methods=['GET'])
def get_productos():
    cursor = db.cursor()
    cursor.execute("SELECT CONCAT('Nombre: ', nombre, ', Marca: ', marca) AS producto_con_marca FROM Productos;")
    productos = cursor.fetchall()
    cursor.close()
    return jsonify(productos)

@app.route('/productos', methods=['POST'])
def add_producto():
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
    return 'Producto agregado correctamente', 201

@app.route('/productos', methods=['PUT'])
def update_producto():
    data = request.json
    print("Datos recibidos en PUT:", data)  # Imprimir los datos recibidos en la consola del servidor Flask
    
    codigo_producto = data.get('codigo_producto')
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    marca = data.get('marca')
    modelo = data.get('modelo')
    precio = data.get('precio')
    stock = data.get('stock')

    cursor = db.cursor()
    query = "UPDATE Productos SET Nombre = %s, Descripcion = %s, Marca = %s, Modelo = %s, Precio = %s, Stock = %s WHERE CodigoProducto = %s"
    cursor.execute(query, (nombre, descripcion, marca, modelo, precio, stock, codigo_producto))
    db.commit()
    cursor.close()
    return 'Producto actualizado correctamente', 200

@app.route('/productos', methods=['DELETE'])
def delete_producto():
    data = request.json
    print("Datos recibidos en DELETE:", data)  # Imprimir los datos recibidos en la consola del servidor Flask
    
    codigo_producto = data.get('codigo_producto')

    cursor = db.cursor()
    query = "DELETE FROM Productos WHERE CodigoProducto = %s"
    cursor.execute(query, (codigo_producto,))
    db.commit()
    cursor.close()
    return 'Producto eliminado correctamente', 200

if __name__ == '__main__':
    app.run(debug=True)
