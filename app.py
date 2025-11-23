#Importamos las funciones de archivo 'archivos.py'
from archivos import (
    exportar_guardar_csv, importar_cargar_csv,fusionar_inventario,default_path,save_copy)

csv_path="guardar.csv"
#Es una lista global donde se guardan los productos en memoria
inventario=[]

#FUNCION: Agregar un producto al inventario
def agregar_producto():
    #Validar nombre del producto
    while True:

        nombre=input("Ingrese el nombre del producto: ")
        if nombre != "":
            break
        print("El nombre no puede estar vacío. Intente de nuevo.")
    #validar el precio
    while True:  
        precio=float(input("Ingrese el precio del producto: ")) 
        if precio >= 0:
            break
        print("El precio debe ser mayor que cero. Intente de nuevo.")
    #validar la cantidad
    while True:
        cantidad=int(input("Ingrese la cantidad del producto: "))
        if cantidad >= 0:
            break   
        print("La cantidad no puede ser negativa. Intente de nuevo.")

    #Crear un diccionario del producto
    producto={
    "nombre":nombre,
    "precio":float(precio),
    "cantidad":int(cantidad)
}
    
    #Agregar al inventario
    inventario.append(producto)
    print("Producto agregado correctamente.\n")
    
    return nombre,precio,cantidad
    
#FUNCION: Mostrar el inventario en la pantalla(consola)
def mostrar_inventario(inventario):
    print("\n--- Inventario actual ---")
    
    #Si no hay producto, mostrar mensaje
    if len(inventario)==0:
        print("No hay productos registrados\n")
        return
    
    #Enumerar productos con indice
    for i, producto in enumerate(inventario, start=1):
        print(f"{i}. {producto['nombre']} | Precio: {producto['precio']} | Cantidad: {producto['cantidad']}")
    print()  
    
#FUNCION: Buscar un producto
def buscar_producto():
    print("\n---Bucar el producto---\n")
    nombre_buscar = input("Ingrese el nombre del producto a buscar: ")
    encontrado = False
    
    #Buscar coincidencias por el nombre
    for producto in inventario:
        if producto["nombre"].lower() == nombre_buscar.lower():
            print("\nProducto encontrado:")
            print(f"Nombre: {producto['nombre']}")
            print(f"Precio: {producto['precio']}")
            print(f"Cantidad: {producto['cantidad']}\n")
            encontrado = True
            break

    if not encontrado:
        print("Producto no encontrado.\n")

#FUNCION: Actualizar el producto        
def actualizar_producto(inventario):
    print("\n---Actualizar el producto---\n")
    nombre_buscar = input("Ingrese el nombre del producto a buscar: ")
    encontrado = False
    for producto in inventario:
        if producto["nombre"].lower() == nombre_buscar.lower():
            print("Producto encontrado")
            
            #Solicitar los nuevos valores
            nuevo_precio=int(input("Ingrese el precio nuevo: "))
            nueva_cantidad=int(input("Ingrese la cantidad nueva: "))
            
            #Actualizar los datos
            producto["precio"]=nuevo_precio
            producto["cantidad"]=nueva_cantidad
    
            print("Se actualizo correctamente")
            encontrado= True  
            break
          
    if not encontrado:
        print("El producto no fue encontrado")

#FUNCION: Eliminar un producto
def eliminar_producto():
    print("---Eliminar producto---\n")
    nombre_eliminar = input("Ingrese el nombre del producto a eliminar: ")
    encontrado = False
    for producto in inventario:
        if producto["nombre"].lower() == nombre_eliminar.lower():
            inventario.remove(producto) #Eliminar producto
            print("Producto eliminado correctamente")
            encontrado= True
            break
    if not encontrado:
        print("Producto no encontrado")
     
#FUNCION: Calcular las estadisticas del inventario   
def calcular_estadisticas():
    print("---Calcular estadisticas---\n")
    if len(inventario)==0:
        print("No hay productos para analizar\n")
        return
    
    unidades_totales=len(inventario)  
    valor_total=0
    #Inicializacion de referencias
    producto_mas_caro= inventario[0]
    producto_mayor_stock=inventario[0]
    
    #Recorrer inventario y calcular valores
    for producto in inventario:
        valor_total += producto['precio']*producto['cantidad']
        if producto["precio"] > producto_mas_caro["precio"]:
            producto_mas_caro = producto
        if producto["cantidad"] < producto_mayor_stock["cantidad"]:
            producto_mayor_stock = producto
   
    print(f"Total de productos registrados: {unidades_totales}")
    print(f"Valor total del inventario: {valor_total}")
    print(f"Producto más caro: {producto_mas_caro['nombre']} (${producto_mas_caro['precio']})")
    print(f"Producto más barato: {producto_mayor_stock['nombre']} (${producto_mayor_stock['precio']})\n")    
 
#FUNCION: Guardar inventario en un archivo CSV    
def menu_guardar_csv():
    print("\nGuardando inventario..")
    exportar_guardar_csv(inventario, "guardar.csv")
 
#FUNCION: Cargar inventario desde CSV
def menu_cargar_csv():
    global inventario
    print("\n---Cargar inventario desde CSV---")
    
    #Ruta ingresada o valor por defectp
    ruta = input("Ingrese la ruta del archivo (Enter = copia_guardar.csv): ").strip() or save_copy
    
    #Cagar datos
    datos = importar_cargar_csv(inventario, ruta)  
    
    #Validar si hubo errores
    if not datos:
        print("No se pudieron cargar los datos.\n")
        return

     # Si está vacío
    if len(datos) == 0:
        print("El archivo está vacío. No hay productos para cargar.\n")
        return

    print(f"\nSe encontraron {len(datos)} productos en el archivo.")
    opcion = input("¿Desea sobrescribir el inventario actual? (S/N): ").strip().upper()
    if opcion == "S":
        inventario = datos
        print("Inventario sobrescrito correctamente.\n")
    elif opcion == "N":
        inventario = fusionar_inventario(inventario, datos)
        print("Inventarios fusionados correctamente.\n")
    else:
        print("Opción inválida. No se realizaron cambios.\n")

#MENU PRINCIPAL DEL PROGRAMA
def menu_principal():
    while True: 
        print("---Menu principal---")
        print("1. Agregar producto")
        print("2. Mostrar inventario")    
        print("3. Buscar producto")
        print("4. Actualizar producto")
        print("5. Eliminar producto")
        print("6. Estadisticas del inventario")
        print("7. Guardar CSV")
        print("8. Cargar CSV")
        print("9. Salir")
        
        option = input("Selecciona una opcion (1-9): ")
        if option == "1":
            agregar_producto()
        elif option == "2":
            mostrar_inventario(inventario)
        elif option == "3":
            buscar_producto()
        elif option == "4":
            actualizar_producto(inventario)
        elif option == "5":
            eliminar_producto()        
        elif option == "6":
            calcular_estadisticas()    
        elif option == "7":
            menu_guardar_csv()    
        elif option == "8":
            menu_cargar_csv() 
        elif option == "9": 
            print("Saliendo del programa...")       
            break
        else:
            print("Opcion invalida, intente nuevamente")
            
#Ejecuta menu principal
menu_principal()
