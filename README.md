## Marangatu RS – Robot de Software para descargar comprobantes

Marangatu RS es una herramienta que **automatiza la descarga de comprobantes registrados (VENTAS y COMPRAS)** desde el portal **Marangatu de la SET**. El sistema inicia sesión, busca el módulo correspondiente y descarga los archivos Excel del mes indicado.

Este robot está diseñado para que cualquier persona pueda usarlo, incluso sin conocimientos técnicos.

---

### Requisitos

* Conexión a internet.
* **Usuario y contraseña** del portal Marangatu.
* **Python 3.10** o superior.

---

### Instalación (Windows)

1.  **Descargar e instalar Python**
    * Descargar desde: `https://www.python.org/downloads/`
    * Durante la instalación, marcar la opción:
        > **✔ "Add Python to PATH"**
2.  **Descargar este proyecto (carpeta ZIP)**
3.  **Extraerlo** en cualquier lugar, por ejemplo: `C:\MarangatuRS`
4.  **Abrir la carpeta del proyecto**
    * Click derecho + **"Open in Terminal"** o **"Abrir PowerShell aquí"**.
5.  **Crear el entorno virtual**
    ```bash
    python -m venv venv
    ```
6.  **Activarlo**
    ```bash
    venv\Scripts\activate
    ```
7.  **Instalar dependencias**
    ```bash
    pip install -r requirements.txt
    ```
8.  **Instalar Playwright**
    ```bash
    playwright install
    ```
**¡Listo!** El sistema ya está preparado para usar.

---

### Instalación (Linux – Ubuntu, Mint, Debian)

1.  **Abrir una terminal** dentro de la carpeta del proyecto.
2.  **Crear entorno virtual:**
    ```bash
    python3 -m venv venv
    ```
3.  **Activarlo:**
    ```bash
    source venv/bin/activate
    ```
4.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Instalar Playwright:**
    ```bash
    playwright install
    ```
**Listo.**

---

### Configuración inicial

* Editar el archivo **`config.py`**:
    ```python
    USER = "TU_USUARIO_MARANGATU"
    PASSWORD = "TU_CONTRASEÑA"
    ```
* *El año y el mes se pedirán al iniciar el programa, así que no hace falta editarlo en el código.*

---

### Cómo usar (paso a paso)

1.  **Abrir una terminal** dentro de la carpeta del proyecto.
2.  **Activar el entorno virtual:**
    * **Windows**
        ```bash
        venv\Scripts\activate
        ```
    * **Linux**
        ```bash
        source venv/bin/activate
        ```
3.  **Ejecutar el robot:**
    ```bash
    python main.py
    ```
4.  El sistema preguntará:
    ```
    Ingrese año (ENTER = año actual):
    Ingrese mes (1-12):
    ```
5.  Se abrirá el navegador y el robot hará todo automáticamente:
    * Inicio de sesión
    * Navegación
    * Búsqueda de Ventas
    * Búsqueda de Compras
    * Descarga de Excel

* Los archivos se guardarán en la carpeta: **`descargas/`**
* *Los archivos se abren automáticamente al finalizar.*