import pytest
from src.inventario.app import app, db, Producto

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_post_producto_exitoso(client):
    res = client.post("/api/productos", json={"nombre": "Teclado", "precio": 100, "stock": 5})
    assert res.status_code == 201
    assert res.get_json()["nombre"] == "Teclado"

def test_post_producto_datos_invalidos(client):
    res = client.post("/api/productos", json={"nombre": "SinPrecio"})
    assert res.status_code == 400

def test_get_productos(client):
    client.post("/api/productos", json={"nombre": "Mouse", "precio": 50, "stock": 10})
    res = client.get("/api/productos")
    assert res.status_code == 200
    data = res.get_json()
    assert "productos" in data

def test_put_actualizar_stock(client):
    res = client.post("/api/productos", json={"nombre": "Monitor", "precio": 300, "stock": 2})
    producto_id = res.get_json()["id"]
    res_put = client.put(f"/api/productos/{producto_id}/stock", json={"stock": 8})
    assert res_put.status_code == 200
    assert res_put.get_json()["stock"] == 8

def test_put_producto_no_existente(client):
    res = client.put("/api/productos/999/stock", json={"stock": 10})
    assert res.status_code == 404

def test_delete_producto(client):
    res = client.post("/api/productos", json={"nombre": "CPU", "precio": 200, "stock": 3})
    producto_id = res.get_json()["id"]
    res_del = client.delete(f"/api/productos/{producto_id}")
    assert res_del.status_code == 200
    assert res_del.get_json()["mensaje"] == "Producto eliminado"

def test_delete_producto_inexistente(client):
    res = client.delete("/api/productos/999")
    assert res.status_code == 404