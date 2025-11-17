import os
def generar_archivo(nombre, mb, carpeta_destino):
    os.makedirs(carpeta_destino, exist_ok=True)
    ruta = os.path.join(carpeta_destino, nombre)
    with open(ruta, "wb") as f:
        f.write(b'\0' * mb * 1024 * 1024)
    print(f"Archivo creado: {ruta}")

generar_archivo("archivo_1mb.txt", 1, r"C:\Users\lopez\OneDrive\UAM\Optativas\SSeguridad\Practica2\Archivos")
