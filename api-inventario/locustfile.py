# locustfile.py
from locust import HttpUser, task, between

class InventarioUser(HttpUser):
    wait_time = between(1, 3)  # espera entre tareas para simular usuarios reales

    def on_start(self):
        """
        Método que se ejecuta al iniciar el usuario.
        Aquí podrías autenticar si tu API tuviera login.
        """
        pass  # no hay autenticación en nuestra API actual

    @task(3)
    def listar_productos(self):
        """
        Tarea para obtener lista de productos
        """
        response = self.client.get("/api/productos")
        response.raise_for_status()  # valida que la respuesta sea 2xx

    @task(2)
    def crear_producto(self):
        """
        Tarea para crear un producto
        """
        payload = {"nombre": "Teclado", "precio": 100, "stock": 5}
        response = self.client.post("/api/productos", json=payload)
        response.raise_for_status()

    @task(1)
    def actualizar_stock(self):
        """
        Tarea para actualizar stock de un producto (id=1 como ejemplo)
        """
        payload = {"stock": 10}
        response = self.client.put("/api/productos/1/stock", json=payload)
        response.raise_for_status()

    @task(1)
    def eliminar_producto(self):
        """
        Tarea para eliminar un producto (id=1 como ejemplo)
        """
        response = self.client.delete("/api/productos/1")
        response.raise_for_status()