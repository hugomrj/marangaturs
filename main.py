import os
import subprocess
import config
import platform
from datetime import datetime
from playwright.sync_api import sync_playwright
from auth import login
from navigation import (
    abrir_por_buscador,
    cargar_filtros_comprobantes_registrados,
    descargar_excel_si_existe
)



def abrir_archivo(path):
    if not os.path.exists(path):
        print(f"Archivo no encontrado: {path}")
        return

    sistema = platform.system()

    try:
        if sistema == "Windows":
            os.startfile(path)  # abre con la aplicación predeterminada
        elif sistema == "Darwin":  # macOS
            subprocess.Popen(["open", path])
        else:  # Linux
            subprocess.Popen(
                ["xdg-open", path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        print(f"Abriendo archivo: {path}")

    except Exception as e:
        print(f"No se pudo abrir el archivo automáticamente: {e}")




def main():

    # === Solicitar año con valor por defecto ===
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

    # === Solicitar mes (obligatorio) ===
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
    archivos_descargados = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://marangatu.set.gov.py/eset/login")
        login(page, config.USER, config.PASSWORD)

        page = abrir_por_buscador(context, page, "Consulta De Comprobantes Registrados")

        # Procesar ambos tipos
        for tipo in TIPOS:
            print(f"\n=== Procesando {tipo} ===")

            cargar_filtros_comprobantes_registrados(page, tipo, year, month)
            ruta_excel = descargar_excel_si_existe(page, year, month)


            if ruta_excel:
                archivos_descargados.append(ruta_excel)

            page.wait_for_timeout(1500)

        print("\nFIN DEL PROCESO — Todos los Excel descargados.")

        browser.close()

    for archivo in archivos_descargados:
        print("Abriendo:", archivo)
        abrir_archivo(archivo)


if __name__ == "__main__":
    main()
