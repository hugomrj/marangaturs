# navigation.py

import calendar
import config


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






def descargar_excel_si_existe(page, year, month):
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(800)

    boton_excel = page.locator("button", has_text="Excel")

    try:
        boton_excel.wait_for(state="visible", timeout=4000)
    except:
        print("No hay registros — no se mostrará el botón Excel.")
        return None

    # Tipo de registro actual (VENTAS, COMPRAS, etc.)
    tipo_registro = page.locator("#tipoRegistro").input_value() or "DESCONOCIDO"

    print(f"Se encontraron registros ({tipo_registro}). Descargando Excel…")

    with page.expect_download() as descarga_event:
        boton_excel.click()

    descarga = descarga_event.value

    nombre_final = f"{tipo_registro}_{year}_{month:02d}.xlsx"
    ruta_final = f"descargas/{nombre_final}"

    descarga.save_as(ruta_final)

    print("Archivo guardado en:", ruta_final)
    return ruta_final
