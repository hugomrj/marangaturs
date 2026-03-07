# anual.py
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

def descargar_anio():
    current_year = datetime.now().year
    cedula = getattr(config, 'CEDULA', None)
    TIPOS = ["VENTAS", "COMPRAS"]

    print("=== DESCARGA ANUAL (MODO REANUDABLE) ===")

    # 1. Pedir Año
    while True:
        entrada = input(f"Ingrese año (ENTER = {current_year}): ").strip()
        if entrada == "": year = current_year; break
        try: year = int(entrada); break
        except: pass

    # 2. Pedir Mes de Inicio (CLAVE PARA REANUDAR)
    while True:
        entrada = input("¿Desde qué mes empezar? (1-12, ENTER=1): ").strip()
        if entrada == "": start_month = 1; break
        try: 
            start_month = int(entrada)
            if 1 <= start_month <= 12: break
        except: pass

    print(f"\nDescargando desde Mes {start_month} hasta el 12...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://marangatu.set.gov.py/eset/login")
        login(page, config.USER, config.PASSWORD)
        page = abrir_por_buscador(context, page, "Consulta De Comprobantes Registrados")

        # Bucle desde el mes indicado
        for month in range(start_month, 13):
            print(f"\n>>> Procesando Mes {month:02d}...")
            
            for tipo in TIPOS:
                try:
                    print(f"  -> {tipo}...", end=" ")
                    cargar_filtros_comprobantes_registrados(page, tipo, year, month)
                    
                    ruta = descargar_excel_si_existe(page, year, month, cedula=cedula)
                    
                    if ruta: print("OK")
                    else: print("Sin datos")
                    
                except Exception as e:
                    # Si falla, lo intentamos una vez más
                    print(f"FALLÓ. Reintentando...")
                    try:
                        page.reload()
                        page.wait_for_timeout(2000)
                        cargar_filtros_comprobantes_registrados(page, tipo, year, month)
                        ruta = descargar_excel_si_existe(page, year, month, cedula=cedula)
                        if ruta: print("  -> Recuperado OK")
                    except:
                        print("  -> Error persistente, continuando con el siguiente.")

                page.wait_for_timeout(1000)

        print("\n¡Proceso terminado!")
        browser.close()

if __name__ == "__main__":
    descargar_anio()