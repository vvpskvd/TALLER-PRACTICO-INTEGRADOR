# app.py
# API REST con Flask, Flask-SQLAlchemy y flask-paginate
# Cumple: 4 endpoints CRUD básicos con persistencia en SQLite

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_paginate import get_page_parameter
import os

app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, '..', 'inventario.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'precio': self.precio,
            'stock': self.stock
        }

# POST /api/productos
@app.route('/api/productos', methods=['POST'])
def crear_producto():
    if not request.is_json:
        return jsonify({'error': 'Payload debe ser JSON'}), 400
    data = request.get_json()
    nombre = data.get('nombre')
    precio = data.get('precio')
    stock = data.get('stock', 0)
    if not nombre or precio is None:
        return jsonify({'error': 'Faltan campos requeridos'}), 400
    try:
        p = Producto(nombre=nombre, precio=float(precio), stock=int(stock))
    except ValueError:
        return jsonify({'error': 'precio y stock deben ser numéricos'}), 400
    db.session.add(p)
    db.session.commit()
    return jsonify(p.to_dict()), 201

# GET /api/productos
@app.route('/api/productos', methods=['GET'])
def listar_productos():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = request.args.get('per_page', type=int, default=10)
    query = Producto.query.order_by(Producto.id)
    total = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    return jsonify({
        'productos': [p.to_dict() for p in items],
        'pagination': {'page': page, 'per_page': per_page, 'total': total}
    })

# PUT /api/productos/{id}/stock
@app.route('/api/productos/<int:producto_id>/stock', methods=['PUT'])
def actualizar_stock(producto_id):
    if not request.is_json:
        return jsonify({'error': 'Payload debe ser JSON'}), 400
    data = request.get_json()
    if 'stock' not in data:
        return jsonify({'error': 'Falta campo stock'}), 400
    producto = db.session.get(Producto, producto_id)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404
    try:
        producto.stock = int(data['stock'])
    except ValueError:
        return jsonify({'error': 'stock debe ser entero'}), 400
    db.session.commit()
    return jsonify(producto.to_dict()), 200

# DELETE /api/productos/{id}
@app.route('/api/productos/<int:producto_id>', methods=['DELETE'])
def eliminar_producto(producto_id):
    producto = db.session.get(Producto, producto_id)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404
    db.session.delete(producto)
    db.session.commit()
    return jsonify({'mensaje': 'Producto eliminado'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
