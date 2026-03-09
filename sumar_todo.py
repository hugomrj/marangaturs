# sumar_todo.py
import os
import pandas as pd
import glob

def obtener_suma(df, palabras_clave):
    """
    Busca una columna que contenga todas las palabras clave en su nombre
    y devuelve la suma numérica de esa columna.
    """
    for col in df.columns:
        # Verificamos si todas las palabras clave están en el nombre de la columna
        col_clean = str(col).strip().lower()
        if all(palabra.lower() in col_clean for palabra in palabras_clave):
            return pd.to_numeric(df[col], errors='coerce').sum()
    return 0

def procesar_resumen():
    carpeta_descargas = "descargas"
    archivos = glob.glob(os.path.join(carpeta_descargas, "*.xlsx"))
    
    if not archivos:
        print("No se encontraron archivos Excel en la carpeta 'descargas'.")
        return

    print(f"Se encontraron {len(archivos)} archivos para procesar.\n")

    # Estructura específica para VENTAS (Solo 10% + Cálculo sin IVA)
    totales_ventas = {
        "Monto Gravado 10%": 0,
        "IVA 10%": 0,
        "Monto a Declarar 10% (Sin IVA)": 0 
    }
    
    # Estructura específica para COMPRAS (10% y 5% + Cálculos sin IVA)
    totales_compras = {
        "Monto Gravado 10%": 0,
        "IVA 10%": 0,
        "Monto a Declarar 10% (Sin IVA)": 0,
        "Monto Gravado 5%": 0,
        "IVA 5%": 0,
        "Monto a Declarar 5% (Sin IVA)": 0,
        "Monto No Gravado / Exento": 0,
        "Total Comprobante": 0
    }

    for archivo in archivos:
        nombre_archivo = os.path.basename(archivo)
        print(f"Procesando: {nombre_archivo}...", end=" ")
        
        try:
            df = pd.read_excel(archivo)
            df.columns = [str(c).strip() for c in df.columns]
            
            # --- EXTRAER VALORES BRUTOS DEL EXCEL ---
            # Buscamos las columnas por palabras clave para ser flexibles con el nombre exacto
            
            # 10%
            gravado_10 = obtener_suma(df, ["gravado", "10"])
            iva_10 = obtener_suma(df, ["iva", "10"])
            
            # 5%
            gravado_5 = obtener_suma(df, ["gravado", "5"])
            iva_5 = obtener_suma(df, ["iva", "5"])
            
            # Exento / No Gravado
            exento = obtener_suma(df, ["exento"]) + obtener_suma(df, ["no gravado"])
            
            # Total
            total = obtener_suma(df, ["total"])

            # --- CLASIFICAR Y SUMAR ---
            if "VENTAS" in nombre_archivo.upper():
                # VENTAS: Solo 10% y sus cálculos
                totales_ventas["Monto Gravado 10%"] += gravado_10
                totales_ventas["IVA 10%"] += iva_10
                
                # Cálculo solicitado: Monto Gravado - IVA
                calculo_sin_iva_10 = gravado_10 - iva_10
                totales_ventas["Monto a Declarar 10% (Sin IVA)"] += calculo_sin_iva_10
                
            elif "COMPRAS" in nombre_archivo.upper():
                # COMPRAS: Todo (10% y 5%)
                # 10%
                totales_compras["Monto Gravado 10%"] += gravado_10
                totales_compras["IVA 10%"] += iva_10
                totales_compras["Monto a Declarar 10% (Sin IVA)"] += (gravado_10 - iva_10)
                
                # 5%
                totales_compras["Monto Gravado 5%"] += gravado_5
                totales_compras["IVA 5%"] += iva_5
                totales_compras["Monto a Declarar 5% (Sin IVA)"] += (gravado_5 - iva_5)
                
                # Otros
                totales_compras["Monto No Gravado / Exento"] += exento
                totales_compras["Total Comprobante"] += total
            else:
                print("Tipo desconocido, ignorando.")
                continue
            
            print("OK")

        except Exception as e:
            print(f"ERROR ({e})")

    # --- MOSTRAR RESULTADOS ---
    print("\n" + "="*60)
    print("RESUMEN FINAL")
    print("="*60)

    print("\n--- TOTAL VENTAS ---")
    print("(Solo 10% según solicitud)")
    for key, value in totales_ventas.items():
        print(f"{key:<35}: {value:,.0f}")

    print("\n--- TOTAL COMPRAS ---")
    print("(Incluye 10% y 5%)")
    for key, value in totales_compras.items():
        print(f"{key:<35}: {value:,.0f}")
        
    # --- GUARDAR EN UN EXCEL NUEVO ---
    # Creamos dataframes separados para que las columnas coincidan con los totales reales
    df_ventas = pd.DataFrame([{"Tipo": "VENTAS", **totales_ventas}])
    df_compras = pd.DataFrame([{"Tipo": "COMPRAS", **totales_compras}])
    
    # Concatenamos. Como tienen columnas distintas, pandas rellenará con NaN donde falte datos,
    # luego lo reemplazamos por 0 o vacío si se desea.
    df_resultado = pd.concat([df_ventas, df_compras], ignore_index=True)
    
    ruta_resumen = os.path.join(carpeta_descargas, "RESUMEN_TOTAL.xlsx")
    df_resultado.to_excel(ruta_resumen, index=False)
    print(f"\nArchivo resumen guardado en: {ruta_resumen}")

if __name__ == "__main__":
    procesar_resumen()