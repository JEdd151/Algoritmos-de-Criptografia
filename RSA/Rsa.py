import time, os
from Crypto.PublicKey import RSA

###GENERACION DE CLAVES
def generar_claves(bits=1024):
    
    key = RSA.generate(bits)

    n, e, d = key.n, key.e, key.d

    os.makedirs("Produccion/", exist_ok=True)

    
    with open("Produccion/clave_publica.txt", "w") as pub:
        pub.write(f"{n},{e}")
    
    with open("Produccion/clave_privada.txt", "w") as priv:
        priv.write(f"{n},{d}")
    
    return (n, e), (n, d)

####CIFRADO
def cifra(mensaje, clave_publica):
    n, e = clave_publica
    inicio = time.perf_counter()
    ###si es número, conviértelo a string
    if isinstance(mensaje, int):
        mensaje = str(mensaje)
    cifrado = [pow(ord(c), e, n) for c in mensaje]
    fin = time.perf_counter()
    with open("Produccion/mensaje_cifrado.txt", "w") as f:
        f.write(",".join(map(str, cifrado)))
    return cifrado, fin - inicio

###DESCIFRADO
def descifrar(cifrado, clave_privada):
    n, d = clave_privada
    inicio = time.perf_counter()
    descifrado = "".join(chr(pow(c, d, n)) for c in cifrado)
    fin = time.perf_counter()
    return descifrado, fin - inicio

###PRUEBAS
def pruebas(archivo, clave_publica, clave_privada, repeticiones=6):
    with open(archivo, "r", encoding="utf-8", errors="ignore") as f:
        contenido = f.read()

    tamaño_mb = os.path.getsize(archivo) / (1024 * 1024)

    tiempos_cifrado = []
    tiempos_descifrado = []
    
    print("-" * 50)
    print(f"\nArchivo: {archivo}")
    print(f"Tamaño: {tamaño_mb:.2f} MB")
    print(f"Realizando {repeticiones} repeticiones de pruebas...\n")
    
    for i in range(repeticiones):
        print(f"Repetición {i+1}/{repeticiones}...", end=" ")
        
        ###cifrado
        _, tiempo_cif = cifra(contenido, clave_publica)
        tiempos_cifrado.append(tiempo_cif)
        
        ###leer el cifrado para descifrarlo
        with open("Produccion/mensaje_cifrado.txt", "r") as f:
            cifrado = [int(x) for x in f.read().strip().split(",") if x]
        
        ###descifrado
        _, tiempo_des = descifrar(cifrado, clave_privada)
        tiempos_descifrado.append(tiempo_des)
        
        print(f"Cifrado: {tiempo_cif:.6f}s, Descifrado: {tiempo_des:.6f}s")
    
    ###calcular promedios
    tiempo_promedio_cif = sum(tiempos_cifrado) / len(tiempos_cifrado)
    tiempo_promedio_des = sum(tiempos_descifrado) / len(tiempos_descifrado)
    tiempo_total_promedio = tiempo_promedio_cif + tiempo_promedio_des
    
    print("\n" + "-" * 50)
    print("RESULTADOS:")
    print(f"Tiempo promedio de cifrado: {tiempo_promedio_cif:.6f} s")
    print(f"Tiempo promedio de descifrado: {tiempo_promedio_des:.6f} s")
    print(f"Tiempo total promedio: {tiempo_total_promedio:.6f} s")
    print("-" * 50)

    return tamaño_mb, tiempo_promedio_cif, tiempo_promedio_des

###MENU PRINCIPAL
def menu_principal():
    while True:
        opcion = input("RSA\n1. Cifrar\n2. Descifrar\n3. Pruebas\nElige una opción... ")

        if opcion == "1":
            print("\nGenerando claves...")
            public_key, private_key = generar_claves()
            print("Clave pública y privada guardadas en archivos.")

            mensaje = input("\nEscribe el mensaje o número a cifrar: ")
            cifrado, t1 = cifra(mensaje, public_key)
            print("\nMensaje cifrado guardado en 'mensaje_cifrado.txt'.")
            print(f"Tiempo de cifrado: {t1:.6f}s")

        elif opcion == "2":
            try:
                with open("Produccion/clave_privada.txt", "r") as f:
                    n_str, d_str = f.read().strip().split(",")
                    private_key = (int(n_str), int(d_str))

                with open("Produccion/mensaje_cifrado.txt", "r") as f:
                    cifrado = [int(x) for x in f.read().strip().split(",") if x]
                
                descifrado, t2 = descifrar(cifrado, private_key)
                print("\nMensaje descifrado:", descifrado)
                print(f"Tiempo de descifrado: {t2:.6f}s")
            
            except Exception as e:
                print("\nError al descifrar:", e)
        
        elif opcion == "3":
            pub, priv = generar_claves(1024)
            archivos = ["C:\\Users\\lopez\\OneDrive\\UAM\\Optativas\\SSeguridad\\Practica2\\Archivos\\archivo_0mb.bin"] ##Modificar el archivo 
            resultados = []

            for archivo in archivos:
                resultados.append(pruebas(archivo, pub, priv))
            break
        else:
            break



if __name__ == "__main__":
    menu_principal()
