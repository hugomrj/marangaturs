# navigation.py

import calendar
import config
import os

def abrir_por_buscador(context, page, texto):
    page.wait_for_load_state("networkidle")

    buscador = page.locator("input[name='busqueda']")
    buscador.fill(texto)
    page.wait_for_timeout(500)

    # Capturar nueva pestaña
    with context.expect_page() as tab_info:
        opcion = page.locator(".list-group-item .ng-binding", has_text=texto).first
        opcion.click()

    nueva_page = tab_info.value
    nueva_page.wait_for_load_state("networkidle")

    return nueva_page

def cargar_filtros_comprobantes_registrados(page, tipo_registro, year, month):
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(400)

    # 1. Seleccionar tipo de registro dinámicamente
    page.select_option("#tipoRegistro", tipo_registro)

    # 2. Construir fechas dinámicas
    fecha_desde = f"01/{month:02d}/{year}"
    ultimo_dia = calendar.monthrange(year, month)[1]
    fecha_hasta = f"{ultimo_dia}/{month:02d}/{year}"

    # 3. Inputs (Angular moment-picker)
    campo_desde = page.locator("input[data-ng-model='vm.datos.filtros.fechaEmisionDesde']")
    campo_hasta = page.locator("input[data-ng-model='vm.datos.filtros.fechaEmisionHasta']")

    campo_desde.click()
    campo_desde.fill(fecha_desde)
    campo_desde.blur()

    campo_hasta.click()
    campo_hasta.fill(fecha_hasta)
    campo_hasta.blur()

    page.wait_for_timeout(300)

    # 4. Ejecutar búsqueda
    page.locator("button[name='busqueda']").click()
    page.wait_for_load_state("networkidle")

# FUNCIÓN UNIFICADA Y MEJORADA
def descargar_excel_si_existe(page, year, month, cedula=None):
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(800)

    boton_excel = page.locator("button", has_text="Excel")

    try:
        # Esperamos un poco más a que el botón aparezca
        boton_excel.wait_for(state="visible", timeout=10000)
    except:
        print("No hay registros — no se mostrará el botón Excel.")
        return None

    tipo_registro = page.locator("#tipoRegistro").input_value() or "DESCONOCIDO"

    print(f"Se encontraron registros ({tipo_registro}). Descargando Excel…")

    try:
        # CONFIGURAMOS UN TIMEOUT LARGO PARA LA DESCARGA (2 minutos)
        with page.expect_download(timeout=120000) as descarga_event:
            # LA CLAVE: no_wait_after=True evita que se congele esperando la navegación
            boton_excel.click(timeout=60000, no_wait_after=True)

        descarga = descarga_event.value
        
        # --- Lógica de nombre y guardado ---
        parte_cedula = f"_{cedula}" if cedula else ""
        nombre_final = f"{tipo_registro}{parte_cedula}_{month:02d}_{year}.xlsx"
        
        # Crear carpeta si no existe (seguridad extra)
        if not os.path.exists("descargas"):
            os.makedirs("descargas")

        ruta_final = os.path.join("descargas", nombre_final)
        descarga.save_as(ruta_final)

        print("Archivo guardado en:", ruta_final)
        return ruta_final

    except Exception as e:
        print(f"Error en descarga: {e}")
        return None