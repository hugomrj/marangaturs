def login(page, user, password):
    page.fill("#usuario", user)
    page.fill("#clave", password)
    page.click("button[type=submit]")

    # Esperar a que termine de cargar el dashboard
    page.wait_for_load_state("networkidle")
