from behave import given, when, then
from src.inventario.app import app, db, Producto

@given("una base de datos vacía")
def step_limpiar_db(context):
    with app.app_context():
        db.drop_all()
        db.create_all()
    context.client = app.test_client()

@when('creo un producto con nombre "{nombre}", precio {precio} y stock {stock}')
def step_crear_producto(context, nombre, precio, stock):
    context.response = context.client.post("/api/productos", json={
        "nombre": nombre,
        "precio": float(precio),
        "stock": int(stock)
    })

@then("el producto se crea correctamente")
def step_verificar_creacion(context):
    assert context.response.status_code == 201

@when("consulto la lista de productos")
def step_listar_productos(context):
    context.response = context.client.get("/api/productos")

@then("recibo una lista de productos")
def step_verificar_lista(context):
    data = context.response.get_json()
    assert "productos" in data
    assert isinstance(data["productos"], list)

@when("actualizo el stock del producto con id {id} a {nuevo_stock}")
def step_actualizar_stock(context, id, nuevo_stock):
    context.response = context.client.put(f"/api/productos/{id}/stock", json={
        "stock": int(nuevo_stock)
    })

@then("el stock se actualiza correctamente")
def step_verificar_actualizacion(context):
    assert context.response.status_code == 200
    data = context.response.get_json()
    assert "stock" in data

@when("elimino el producto con id {id}")
def step_eliminar_producto(context, id):
    context.response = context.client.delete(f"/api/productos/{id}")

@then("el producto se elimina correctamente")
def step_verificar_eliminacion(context):
    assert context.response.status_code == 200
    data = context.response.get_json()
    assert data["mensaje"] == "Producto eliminado"

@when("intento crear un producto sin nombre")
def step_crear_producto_invalido(context):
    context.response = context.client.post("/api/productos", json={"precio": 10})

@then("recibo un error de validación")
def step_verificar_error(context):
    assert context.response.status_code == 400