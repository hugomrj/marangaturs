# sumar_todo.py
import os
import pandas as pd
import glob

def procesar_resumen():
    carpeta_descargas = "descargas"
    archivos = glob.glob(os.path.join(carpeta_descargas, "*.xlsx"))
    
    if not archivos:
        print("No se encontraron archivos Excel en la carpeta 'descargas'.")
        return

    print(f"Se encontraron {len(archivos)} archivos para procesar.\n")

    # Diccionarios para guardar los totales
    totales_ventas = {
        "Monto Gravado 10%": 0,
        "IVA 10%": 0,
        "Monto Gravado 5%": 0,
        "IVA 5%": 0,
        "Monto No Gravado / Exento": 0,
        "Total Comprobante": 0
    }
    
    totales_compras = totales_ventas.copy() # Mismo esquema
    
    # Lista de columnas a sumar (basado en tus imágenes)
    columnas_objetivo = [
        "Monto Gravado 10%", 
        "IVA 10%", 
        "Monto Gravado 5%", 
        "IVA 5%", 
        "Monto No Gravado / Extento", # Ojo con la ortografía del sistema (Extento vs Exento)
        "Total Comprobante"
    ]

    for archivo in archivos:
        nombre_archivo = os.path.basename(archivo)
        print(f"Procesando: {nombre_archivo}...", end=" ")
        
        try:
            # Leer el Excel. Se asume que el encabezado está en la fila 0
            df = pd.read_excel(archivo)
            
            # Limpiar nombres de columnas (quitar espacios extras)
            df.columns = [str(c).strip() for c in df.columns]
            
            # Detectar si es VENTA o COMPRA
            if "VENTAS" in nombre_archivo.upper():
                totales = totales_ventas
            elif "COMPRAS" in nombre_archivo.upper():
                totales = totales_compras
            else:
                print("Tipo desconocido, ignorando.")
                continue

            # Sumar las columnas si existen
            for col in columnas_objetivo:
                # Buscamos la columna coincidente (a veces cambia mayúsculas o espacios)
                col_real = next((c for c in df.columns if col.lower() in c.lower()), None)
                
                if col_real:
                    # Convertir a número y sumar, ignorando errores
                    valor = pd.to_numeric(df[col_real], errors='coerce').sum()
                    if not pd.isna(valor):
                        # Usamos la clave limpia para nuestro diccionario
                        totales[col] += valor
            
            print("OK")

        except Exception as e:
            print(f"ERROR ({e})")

    # --- MOSTRAR RESULTADOS ---
    print("\n" + "="*50)
    print("RESUMEN FINAL")
    print("="*50)

    print("\n--- TOTAL VENTAS ---")
    for key, value in totales_ventas.items():
        print(f"{key:<30}: {value:,.0f}")

    print("\n--- TOTAL COMPRAS ---")
    for key, value in totales_compras.items():
        print(f"{key:<30}: {value:,.0f}")
        
    # --- GUARDAR EN UN EXCEL NUEVO ---
    df_resultado = pd.DataFrame([
        {"Tipo": "VENTAS", **totales_ventas},
        {"Tipo": "COMPRAS", **totales_compras}
    ])
    
    ruta_resumen = os.path.join(carpeta_descargas, "RESUMEN_TOTAL.xlsx")
    df_resultado.to_excel(ruta_resumen, index=False)
    print(f"\nArchivo resumen guardado en: {ruta_resumen}")

if __name__ == "__main__":
    procesar_resumen()


# python sumar_todo.py    