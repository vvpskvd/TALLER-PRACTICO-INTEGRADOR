# API de Inventario

API REST para gestion de inventario desarrollada con **Flask**. Permite crear, listar, actualizar y eliminar productos. Incluye pruebas unitarias, pruebas de comportamiento (BDD), pruebas de carga y configuracion de CI/CD.

---

##  Estructura del Proyecto
api-inventario/
├─ src/inventario/
│ └─ app.py # Aplicacion Flask con endpoints y configuracion de BD
├─ tests/
│ └─ test_app.py # Pruebas unitarias con pytest
├─ features/
│ ├─ inventario.feature # Escenarios BDD en Gherkin
│ └─ steps/inventario_steps.py # Implementacion de steps de Behave
├─ locustfile.py # Plan de pruebas de carga con Locust
├─ Makefile # Script de automatizacion de pipeline
├─ pyproject.toml # Configuracion de Poetry y dependencias
└─ requirements.txt # Dependencias del proyecto

---

## Instalacion

Usando **Poetry**:

```bash
# Instalar dependencias
poetry install

# Activar el entorno virtual
poetry shell

O con pip usando requirements.txt:

pip install -r requirements.txt

---

## Ejecucion de la API

poetry run python src/inventario/app.py

---

## Pruebas

# Pruebas unitarias
poetry run pytest --cov --cov-report=html

Cobertura minima: 85%.

Reporte HTML: htmlcov/index.html.

Uso de pytest-mock para simular dependencias.

* Pruebas de comportamiento (BDD)
* poetry run behave
* poetry run behave --format=html


Escenarios definidos en features/inventario.feature.

Steps implementados en features/steps/inventario_steps.py.

Verifica flujos criticos de la API.


## CI/CD

Pipeline sugerido:

Integracion continua (CI):

Instala dependencias (poetry install).

Ejecuta pruebas unitarias y BDD.

Genera reportes de cobertura y resultados de BDD.

Verifica que cobertura ≥ 85%.

Despliegue continuo (CD):

Despliegue automatico a staging/produccion.

Uso de contenedores Docker opcional.

Variables de entorno para configuracion de la base de datos.

Automatizacion de pruebas de carga:

Locust se puede integrar en CI/CD para validar el trabajo antes de desplegar.


## Metricas y analisis

Cobertura de codigo: Pytest genera reportes HTML.

Flujos de la aplicacion: Verificados con Behave.

Rendimiento: Medido con Locust.

Interpretacion:

Detecta cuellos de botella.

Permite optimizar endpoints y base de datos.

Garantiza estabilidad en produccion.