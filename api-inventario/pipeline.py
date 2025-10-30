# pipeline.py
import subprocess
import sys

def run(cmd):
    """Ejecuta un comando en la terminal y detiene si falla."""
    print(f">> Ejecutando: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"ERROR: Comando falló -> {cmd}")
        sys.exit(result.returncode)

def main():
    # 1. Instalar dependencias
    run("poetry install")

    # 2. Ejecutar pruebas unitarias con cobertura
    run("poetry run pytest --cov --cov-report=html")

    # 3. Ejecutar Behave
    run("poetry run behave")

    # 4. (Opcional) Ejecutar Locust en modo headless y generar CSV
    # run("poetry run locust -f locustfile.py --host=http://localhost:5000 --headless -u 50 -r 2 -t 5m --csv=locust_stats")

if __name__ == "__main__":
    main()