import csv     
import os

#Es el archivo principal donde se guarda el inventario
default_path="guardar.csv"

#Es donde se guarda una copia del inventario cargado 
save_copy="copia_guardar.csv"


#FUNCION: Para guardar el inventario en un archivo CSV
def exportar_guardar_csv(inventario, ruta=default_path, incluir_header=True):
    
    #Sie l inventario esta vacio, no se puede cargar
    if not inventario:
            print("El inventario esta vacio, No puede guardar el archivo CSV")
            return
    try:
        #Abrimos el archivo en modo escritura 'w'
        with open(ruta, mode='w', newline='', encoding='utf-8') as guardar_csv:
            #creamos el archivo csv
            csv_writer=csv.writer(guardar_csv)

            #Para los encabezados
            if incluir_header:
                csv_writer.writerow( ['nombre', 'precio', 'cantidad'])
            #Recorremos cada producto y lo escribimos en el archivo CSV
            for producto in inventario:
                    csv_writer.writerow([
                            producto.get("nombre"),
                            producto.get("precio"),
                            producto.get("cantidad")
                    ])
                    
                    
        print(f"Inventario guardado en: {ruta}" )
        
    except PermissionError:
        print("Error: No se tienen permisos para escribir en la ruta especificada.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")


#FUNCION: Para importar el inventario  desde archivo CSV
def importar_cargar_csv(inventario, ruta=save_copy):
    #Verificar si el archivo existe
    if not os.path.exists(ruta):
        print(f"ERROR: El archivo '{ruta}' no existe. No se cargó nada.\n")
        return inventario

    productos = [] #Una lista donde se guarda los productos leidos
    filas_invalidas = 0 #Contador de filas con errores

    try:
        #Abrimos el archivo en modo lectura
        with open(ruta, 'r', newline='', encoding='utf-8') as archivo:
            reader = csv.DictReader(archivo)

            #validamos el encabezado
            if reader.fieldnames != ["nombre", "precio", "cantidad"]:
                print("Error: encabezado inválido. Debe ser: nombre,precio,cantidad")
                return inventario

            #Procesamos cada fila
            for fila in reader:
                try:
                    nombre = fila["nombre"]
                    precio = float(fila["precio"])
                    cantidad = int(fila["cantidad"])

                    #Validacion de datos incorrectos(precios o cantidades negativas)
                    if precio < 0 or cantidad < 0:
                        raise ValueError

                    #Agregar producto alido a la lista
                    productos.append({
                        "nombre": nombre,
                        "precio": precio,
                        "cantidad": cantidad
                    })

                except:
                    filas_invalidas += 1

    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return inventario

    #Mostrar resumen de lectura
    print(f"\nProductos válidos: {len(productos)} | Filas inválidas: {filas_invalidas}\n")

    #Archivo vacio
    if len(productos) == 0:
        print("El archivo está vacío.\n")
        return inventario

    #  Preguntar si se desea sobrescribir el inventario actual
    opcion = input("¿Sobrescribir inventario? (S/N): ").strip().upper()

    if opcion == "S":
        inventario = productos #Reemplaza la lista original
        
        #Guardar tambien una copia en copia_guardar.csv
        with open("copia_guardar.csv", 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["nombre", "precio", "cantidad"])
            for prod in inventario:
                writer.writerow([prod["nombre"], prod["precio"], prod["cantidad"]])
        print("Inventario reemplazado.\n")
    else:
        print("Inventario NO fue sobrescrito.\n")

 

# FUNCION:  Fusionar inventarios (sumar cantidades)
def fusionar_inventario(inventario, productos_nuevos):
    # # Convertir inventario actual a diccionario usando el nombre como clave
    inventario_dic = {p["nombre"].lower(): p for p in inventario}

    #Recorre productos nuevos
    for prod in productos_nuevos:
        nombre = prod["nombre"].lower()

        if nombre in inventario_dic:
            # Sumar cantidades si el producto ya existe
            inventario_dic[nombre]["cantidad"] += prod["cantidad"]
            # Actualizar precio al precio nuevo
            inventario_dic[nombre]["precio"] = prod["precio"]
        else:
            # Si no existe, agregar producto
            inventario_dic[nombre] = prod

    print("Inventario fusionado.")
    return list(inventario_dic.values())
