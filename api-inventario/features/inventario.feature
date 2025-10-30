Feature: Gestión de inventario

  Scenario: Crear producto exitosamente
    Given una base de datos vacía
    When creo un producto con nombre "Teclado", precio 100 y stock 5
    Then el producto se crea correctamente

  Scenario: Listar productos
    Given una base de datos vacía
    When creo un producto con nombre "Mouse", precio 50 y stock 10
    And consulto la lista de productos
    Then recibo una lista de productos

  Scenario: Actualizar stock de producto
    Given una base de datos vacía
    When creo un producto con nombre "Monitor", precio 300 y stock 2
    And actualizo el stock del producto con id 1 a 8
    Then el stock se actualiza correctamente

  Scenario: Eliminar producto
    Given una base de datos vacía
    When creo un producto con nombre "CPU", precio 200 y stock 3
    And elimino el producto con id 1
    Then el producto se elimina correctamente

  Scenario: Error al crear producto sin nombre
    Given una base de datos vacía
    When intento crear un producto sin nombre
    Then recibo un error de validación