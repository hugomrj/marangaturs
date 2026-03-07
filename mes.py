import os
import config
from datetime import datetime
from playwright.sync_api import sync_playwright
from auth import login
from navigation import (
    abrir_por_buscador,
    cargar_filtros_comprobantes_registrados,
    descargar_excel_si_existe
)

def main():
    # === 1. Crear carpeta 'descargas' si no existe ===
    if not os.path.exists("descargas"):
        os.makedirs("descargas")
        print("Carpeta 'descargas' creada correctamente.")

    # === 2. Solicitar año ===
    current_year = datetime.now().year
    while True:
        entrada = input(f"Ingrese año (ENTER = {current_year}): ").strip()
        if entrada == "":
            year = current_year
            break
        try:
            year = int(entrada)
            if 2000 <= year <= 2100:
                break
            print("Año inválido.")
        except ValueError:
            print("Debe ser un número.")

    # === 3. Solicitar mes ===
    while True:
        entrada = input("Ingrese mes (1-12): ").strip()
        try:
            month = int(entrada)
            if 1 <= month <= 12:
                break
            print("Mes inválido.")
        except ValueError:
            print("Debe ser un número.")

    print("\nUsando configuración:")
    print("Usuario:", config.USER)
    print("Año:", year)
    print("Mes:", month)

    TIPOS = ["VENTAS", "COMPRAS"]
    
    # Intentamos obtener cédula de config si existe
    cedula = getattr(config, 'CEDULA', None)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://marangatu.set.gov.py/eset/login")
        login(page, config.USER, config.PASSWORD)

        page = abrir_por_buscador(context, page, "Consulta De Comprobantes Registrados")

        # Procesar ambos tipos (Ventas y Compras)
        for tipo in TIPOS:
            print(f"\n=== Procesando {tipo} ===")

            cargar_filtros_comprobantes_registrados(page, tipo, year, month)
            
            # Pasamos la cédula si está configurada
            ruta_excel = descargar_excel_si_existe(page, year, month, cedula=cedula)

            if ruta_excel:
                print(f"Guardado: {ruta_excel}")
            else:
                print("No se encontraron registros.")

            page.wait_for_timeout(1500)

        print("\nFIN DEL PROCESO — Archivos guardados en la carpeta 'descargas'.")
        browser.close()

if __name__ == "__main__":
    main()