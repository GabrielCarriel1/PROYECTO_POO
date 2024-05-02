from components import Menu,Valida
from utilities import borrarPantalla,gotoxy
from utilities import reset_color,red_color,green_color,yellow_color,blue_color,purple_color,cyan_color
from clsJson import JsonFile
from company  import Company
from customer import RegularClient, VipClient, Client
from sales import Sale
from product  import Product
from iCrud import ICrud
import datetime
import time,os
from functools import reduce


path, _ = os.path.split(os.path.abspath(__file__))
# Procesos de las Opciones del Menu Facturacion
class CrudClients(ICrud):
    def __init__(self, json_file_path):
        self.json_file = JsonFile(json_file_path)
    
    def create(self):
        while True:  
            borrarPantalla()  
            
            # Validación
            valida = Valida()
            
            # Título
            gotoxy(2, 1)
            print("\033[1;32m" + "█" * 90)  # Línea verde
            gotoxy(2, 2)
            print("██" + " " * 34 + "Menú de Creación de Clientes" + " " * 25 + "██")
            gotoxy(3, 1)
            print("\033[1;32m" + "█" * 90)  # Línea verde

            # Solicitar nombres del cliente
            while True:
                gotoxy(5, 4)
                print("\033[K", end='')  # Limpiar línea
                nombre = input("Ingrese los nombres del cliente: ")
                if valida.validar_nombres(nombre):
                    break
                print("\033[31mError: Ingrese solo letras sin caracteres especiales o números\033[0m")
                time.sleep(2)
            
            # Solicitar apellidos del cliente
            while True:
                gotoxy(5, 6)
                print("\033[K", end='')  # Limpiar línea
                apellido = input("Ingrese los apellidos del cliente: ")
                if valida.validar_apellidos(apellido):
                    break
                print("\033[31mError: Ingrese solo letras sin caracteres especiales o números\033[0m")
                time.sleep(2)

            # Solicitar DNI del cliente
            while True:
                gotoxy(5, 8)
                print("\033[K", end='')  # Limpiar línea
                dni = input("Ingrese el DNI del cliente: ")
                if valida.validar_cedula(dni):
                    break
                print("\033[31mError: DNI o RUC incorrecto. Digite un número válido.\033[0m")
                time.sleep(2)

            # Preguntar si el cliente es VIP
            gotoxy(5, 10)
            es_vip = input("¿Es un cliente VIP? (si/no): ").strip().lower() == 'si'

           
            if not es_vip:
                gotoxy(5, 12)
                es_regular = input("¿Es un cliente regular? (si/no): ").strip().lower() == 'si'
            else:
                es_regular = False

            
            if es_vip:
               
                cliente = VipClient(nombre, apellido, dni)
                
                gotoxy(5, 14)
                limite = input("Ingrese el límite de crédito del cliente VIP (10000-20000): ")
                cliente.limit = int(limite)  
            elif es_regular:
               
                cliente = RegularClient(nombre, apellido, dni, card=True)
            else:
                
                cliente = Client(nombre, apellido, dni)

            
            json_file = JsonFile(path + '/archivos/clients.json')
            clientes = json_file.read()

           
            for cliente_existente in clientes:
                if cliente_existente["dni"] == dni:
                    gotoxy(5, 16)
                    print("\033[K", end='')  # Limpiar línea
                    print("\033[31mError: El cliente con este DNI ya existe. Intente nuevamente.\033[0m")
                    time.sleep(2)
                    break
            
            else:
                # Agregar el cliente a la lista
                clientes.append(cliente.getJson())

                # Guardar clientes en el archivo JSON
                json_file.save(clientes)

                # Mostrar mensaje de éxito
                gotoxy(5, 18)
                print("\033[32mCliente ingresado correctamente.\033[0m")
            
           
            gotoxy(5, 20)
            decision = input("\033[32m¿Desea crear otro cliente? (si/no): \033[0m").strip().lower()
            if decision == 'no':
                break


    
    def update(self):
        
        while True:
            borrarPantalla()
            valida = Valida()
            dni = input("Ingrese el DNI del cliente a actualizar: ")

            # Leer los clientes de la base de datos
            json_file = JsonFile(path + '/archivos/clients.json')
            clientes = json_file.read()
            
            # Buscar el cliente por DNI
            cliente_encontrado = None
            for cliente in clientes:
                if cliente["dni"] == dni:
                    cliente_encontrado = cliente
                    break

            if not cliente_encontrado:
                print("\033[31mError: No se encontró un cliente con ese DNI.\033[0m")
                return

            # Mostrar el cliente encontrado en formato de tabla con asteriscos
            # Define el formato de la tabla
            encabezados = f"\033[1m| {'NOMBRES':<15} | {'APELLIDOS':<15} | {'CÉDULA':<15} | {'TARJETA DE DESCUENTO':<15} |\033[0m"
            separador = "\033[1;34m" + "*" * 75 + "\033[0m"
            
            # Imprime el separador y el encabezado de la tabla
            print(separador)
            print(encabezados)
            print(separador)
            
            # Verifica si el cliente tiene tarjeta de descuento
            tarjeta_texto = 'Sí' if cliente_encontrado.get('valor') == 0.10 else 'No'
            
            # Imprime la información del cliente en formato de tabla
            print(f"| {cliente_encontrado['nombre']:<15} | {cliente_encontrado['apellido']:<15} | {cliente_encontrado['dni']:<15} | {tarjeta_texto:<15} |")
            
            # Imprime el separador final de la tabla
            print(separador)

            # Determinar el tipo de cliente
            if "valor" in cliente_encontrado:
                cliente_tipo = "Regular" if cliente_encontrado["valor"] == 0.10 else "VIP"
            else:
                cliente_tipo = "Final"

            print(f"Tipo de cliente: {cliente_tipo}")

            # Actualizar datos generales
            nuevo_nombre = input(f"Nombre actual ({cliente_encontrado['nombre']}): ")
            if nuevo_nombre:
                cliente_encontrado["nombre"] = nuevo_nombre

            nuevo_apellido = input(f"Apellido actual ({cliente_encontrado['apellido']}): ")
            if nuevo_apellido:
                cliente_encontrado["apellido"] = nuevo_apellido

            

            while True:
        # Solicitar el nuevo DNI al usuario
                nuevo_dni = input(f"DNI actual ({cliente_encontrado['dni']}): ")

        # Verificar si se proporcionó un nuevo DNI
                if nuevo_dni:
            # Validar el nuevo DNI
                    if valida.validar_cedula(nuevo_dni):
                # Si el nuevo DNI es válido, actualiza el DNI del cliente
                        cliente_encontrado["dni"] = nuevo_dni
                        break
                    else:
                # Mostrar mensaje de error si el DNI es inválido
                        print("\033[31mError: DNI o RUC incorrecto. Digite un número válido.\033[0m")
                # Esperar unos segundos para que el usuario lea el mensaje
                        time.sleep(2)
                # Borrar la línea de error
                        print("\033[K", end='', flush=True)  # Esto borra la línea del mensaje de error

            # Actualizar datos específicos según el tipo de cliente
            if cliente_tipo == "Regular":
                nueva_tarjeta = input(f"El cliente tiene tarjeta de descuento? (si/no, actual: {'si' if cliente_encontrado['valor'] == 0.10 else 'no'}): ").strip().lower()
                if nueva_tarjeta == "si":
                    cliente_encontrado["valor"] = 0.10
                else:
                    cliente_encontrado["valor"] = 0

            elif cliente_tipo == "VIP":
                while True:
                    try:
                        nuevo_limite = int(input(f"Límite de crédito actual ({cliente_encontrado['valor']}): "))
                        if 1000 <= nuevo_limite <= 2000:
                            cliente_encontrado["valor"] = nuevo_limite
                            break
                        else:
                            print("\033[31mError: El límite de crédito debe estar entre 1000 y 2000.\033[0m")
                    except ValueError:
                        print("\033[31mError: Ingrese un valor numérico válido para el límite de crédito.\033[0m")

            # Actualizar la base de datos
            json_file.save(clientes)

            print("\033[32mCliente actualizado correctamente.\033[0m")

            decision = input("\033[32m¿Desea Actualizar otro cliente? (si/no): \033[0m").strip().lower()
            if decision == 'no':
                break

    def delete(self):
        while True:
            borrarPantalla()

            # Leer archivo JSON
            json_file = JsonFile(path + '/archivos/clients.json')
            clientes = json_file.read()
            
            # Solicitar DNI del cliente a eliminar
            dni = input("Ingrese el DNI del cliente a eliminar: ")
            
            # Inicializar variables
            cliente_encontrado = None

            # Buscar el cliente por DNI
            for c in clientes:
                if c["dni"] == dni:
                    # Si se encuentra el cliente, guarda la referencia del cliente encontrado
                    cliente_encontrado = c
                    break

            # Si se encuentra un cliente con el DNI
            if cliente_encontrado is not None:
                # Determinar el tipo de cliente
                if "valor" in cliente_encontrado:
                    if isinstance(cliente_encontrado["valor"], int):  # Cliente VIP
                        cliente_tipo = "VIP"
                        info_adicional = f"Límite de crédito: {cliente_encontrado['valor']}"
                    else:  # Cliente regular
                        cliente_tipo = "Regular"
                        info_adicional = "Tiene tarjeta de descuento"
                else:
                    cliente_tipo = "Final"
                    info_adicional = "Cliente final"

                # Mostrar información del cliente eliminado en formato de tabla
                print("\033[1;34m" + "-" * 61 + "\033[0m")
                print(f"\033[1m| {'TIPO DE CLIENTE':<12} | {'NOMBRE':<12} | {'APELLIDO':<12} | {'CÉDULA':<12} |\033[0m")
                print("\033[1;34m" + "-" * 61 + "\033[0m")
                
                # Mostrar la información del cliente
                print(f"| {cliente_tipo:<12} | {cliente_encontrado['nombre']:<12} | {cliente_encontrado['apellido']:<12} | {cliente_encontrado['dni']:<12} |")
                print("\033[1;34m" + "-" * 61 + "\033[0m")
                
                # Mostrar información adicional según el tipo de cliente
                print(f"\033[33mInformación adicional: {info_adicional}\033[0m")
                
                # Preguntar al usuario si quiere eliminar al cliente
                gotoxy(1, 8); confirmacion = input("\033[33m¿Está seguro que quiere eliminar al cliente? (Dígite Si o No): \033[0m").lower()
                
                # Si la respuesta es sí, eliminar el cliente
                if confirmacion == 'si':
                    # Eliminar el cliente de la lista de clientes
                    clientes.remove(cliente_encontrado)
                    # Guardar los clientes restantes en el archivo JSON
                    json_file.save(clientes)
                    gotoxy(1,10);print("\033[32mCliente eliminado con éxito ✅\033[0m")
                else:
                    gotoxy(1,10);print("\033[32mEl cliente no ha sido eliminado.\033[0m")
            else:
                gotoxy(1,10);print("\033[31mCliente no encontrado, ingrese un DNI correcto.\033[0m")
            
            # Esperar un momento antes de continuar
            gotoxy(1, 12)
            decision = input("\033[32m¿Desea eliminar otro cliente? (si/no): \033[0m").strip().lower()
            if decision == 'no':
                break


    def consult(self):
        # Consultar información de un cliente
        borrarPantalla()
        json_file = JsonFile(path + '/archivos/clients.json')
        clientes = json_file.read()

        gotoxy(2, 2); print("Consultar un cliente:")
        dni = input("Ingrese el DNI del cliente a consultar: ")
        
        # Buscar el cliente por DNI
        cliente = None
        for c in clientes:
            if c["dni"] == dni:
                cliente = c
                break

        # Si el cliente no fue encontrado
        if cliente is None:
            gotoxy(2, 5); print("Cliente no encontrado.")
            input("Presione enter para regresar al menú. ")
            return

        borrarPantalla()

        # Determinar el tipo de cliente
        if "valor" in cliente:
            if cliente["valor"] == 0.10:
                cliente_tipo = "Regular"
            else:
                cliente_tipo = "VIP"
        else:
            cliente_tipo = "Final"

        # Mostrar encabezado con el tipo de cliente
        print("\033[1;34m" + f" Cliente encontrado (Tipo: {cliente_tipo}) ".center(50, "=") + "\033[0m")

        # Crear un formato de tabla con encabezados
        print("\033[1;34m" + "-" * 45 + "\033[0m")
        # Cambiar el color del mensaje a verde
        print(f"\033[34m\033[1m| {'Campo':<20} | {'Información':<18} |\033[0m")

        print("\033[1;34m" + "-" * 45 + "\033[0m")

        # Imprimir los datos del cliente en la tabla
        print(f"\033[33m| {'NOMBRE':<20} | {cliente['nombre']:<18} |\033[0m")
        print("\033[33m" + "-" * 45 + "\033[0m")
        print(f"\033[33m| {'APELLIDO':<20} | {cliente['apellido']:<18} |\033[0m")
        print("\033[33m" + "-" * 45 + "\033[0m")
        print(f"\033[33m| {'CÉDULA':<20} | {cliente['dni']:<18} |\033[0m")
        print("\033[33m" + "-" * 45 + "\033[0m")


        # Dependiendo del tipo de cliente, mostrar información adicional
        if cliente_tipo == "Regular":
            # Mostrar si el cliente tiene tarjeta de descuento
            tarjeta_texto = 'Sí' if cliente['valor'] == 0.10 else 'No'
            print(f"| {'Tarjeta de descuento':<20} | {tarjeta_texto:<18} |")
        elif cliente_tipo == "VIP":
            # Mostrar el límite de crédito del cliente VIP
            print(f"\033[33m| {'LÍMITE DE CRÉDITO':<20} | {cliente['valor']:<18} |\033[0m")
        # Cerrar la tabla con una línea de separación inferior
        print("\033[1;34m" + "-" * 45 + "\033[0m")

        # Esperar a que el usuario presione enter para regresar al menú
        input("Presione enter para regresar al menú. ")

    def all_consult(self):
        # Borrar pantalla
        borrarPantalla()
        
        # Leer los clientes del archivo JSON
        json_file = JsonFile(path + '/archivos/clients.json')
        clientes = json_file.read()
        
        # Verificar si hay clientes
        if not clientes:
            print("\033[31mNo hay clientes para mostrar.\033[0m")
        else:
            print("\033[1;34m" + "=" * 45 + "\033[0m")
            print(f"\033[1m| {'Nombre':<15} | {'Apellido':<15} | {'DNI':<15} |\033[0m")
            print("\033[1;34m" + "=" * 45 + "\033[0m")
            
            # Mostrar información de cada cliente
            for cliente in clientes:
                print(f"| {cliente['nombre']:<15} | {cliente['apellido']:<15} | {cliente['dni']:<15} |")
                print("\033[1;34m" + "-" * 45 + "\033[0m")
        
        # Esperar a que el usuario presione una tecla para regresar al menú
        input("\033[32mPresione una tecla para regresar al menú.\033[0m")


    
        

class CrudProducts(ICrud):
    def __init__(self, json_file_path):
        self.json_file = JsonFile(json_file_path)

    def create(self):
        borrarPantalla()
        
        # Crear un nuevo producto
        gotoxy(2, 1)
        print("\033[1;35m" + "█" * 90)
        gotoxy(2, 2)
        print("██" + " " * 34 + "Menú de Creación de Productos" + " " * 25 + "██")
        gotoxy(3, 1)
        print("\033[1;35m" + "█" * 90)
        
        # Solicitar datos del producto
        gotoxy(5, 4)
        descripcion = input("Ingrese el nombre del producto: ")
        gotoxy(5, 6)
        precio = float(input("Ingrese el precio: "))
        gotoxy(5, 8)
        stock = int(input("Cantidad en stock: "))

        # Leer datos de productos existentes
        json_file = JsonFile(path + '/archivos/products.json')
        productos = json_file.read()

        # Obtener el próximo ID disponible
        if productos:
            nuevo_id = productos[-1]['id'] + 1
        else:
            nuevo_id = 1

        # Crear una nueva instancia de Product
        producto = Product(nuevo_id, descripcion, precio, stock)

        # Agregar el nuevo producto a la lista de productos
        productos.append(producto.getJson())

        # Guardar los productos actualizados en el archivo JSON
        json_file.save(productos)

        gotoxy(5, 10)
        print("Producto agregado con éxito.")
        gotoxy(5, 12)
        input("Presione Enter para regresar.")

    def update(self):
        while True:
            # Actualizar un producto existente
            borrarPantalla()
            gotoxy(2, 2); print("Actualizar un producto existente:")
            id_producto = int(input("Ingrese el ID del producto a actualizar: "))
            
            json_file = JsonFile(path + '/archivos/products.json')
            productos = json_file.read()
            
            if not productos:
                gotoxy(2, 5); print("Producto no encontrado.")
                time.sleep(2)
                return
            
            producto_encontrado = None
            for p in productos:
                if p['id'] == id_producto:
                    producto_encontrado = p
                    break
            if not producto_encontrado:
                print("\033[31mError: No se encontró un productocon ese ID.\033[0m")
                return

            encabezados = f"\033[1m| {'ID':<15} | {'DESCRIPCIÓN':<15} | {'PRECIP':<15} | {'STOCK':<15} |\033[0m"
            separador = "\033[1;34m" + "*" * 75 + "\033[0m" 

            print(separador)
            print(encabezados)
            print(separador)


            
            print(f"| {producto_encontrado['id']:<15} | {producto_encontrado['descripcion']:<15} | {producto_encontrado['precio']:<15} | {producto_encontrado['stock']:<15} |")           
            
            print(separador)
            
                
            print(f"ID actual: ({producto_encontrado['id']})")

            nueva_descripcion = input(f"Descripcion actual ({producto_encontrado['descripcion']}) Ingresar una nueva descripcion: ")
            producto_encontrado['descripcion'] = nueva_descripcion
            nuevo_precio = input(f"Precio actual ({producto_encontrado['precio']}) Ingresar un nuevo precio: ")
            producto_encontrado['precio'] = nuevo_precio
            actualizar_stock = input(f"Stock actual ({producto_encontrado['stock']}) Actualice el stock: ")
            producto_encontrado['stock'] = actualizar_stock
                

            json_file.save(productos)
            gotoxy(1, 12); print("Producto actualizado con éxito.")
            
            gotoxy(1, 14)
            decision = input("\033[32m¿Desea actualizar otro producto? (si/no): \033[0m").strip().lower()
            if decision == 'no':
                break

    def delete(self):
        while True:
            borrarPantalla()
            valida = Valida()
            # Eliminar un producto específico
            json_file = JsonFile(path + '/archivos/products.json')
            productos = json_file.read()
            # Título
            gotoxy(0, 1)
            print("\033[1;36m" + "█" * 90)  # Línea verde
            gotoxy(1, 2)
            print("██" + " " * 34 + "Eliminar producto" + " " * 36 + "██")
            gotoxy(2, 1)
            print("\033[1;36m" + "█" * 90)  # Línea verde

           
                
            gotoxy(5,6);id_producto = int(input("Ingrese el ID del producto a eliminar: "))

            producto_encontrado = None
            for p in productos:
                if p["id"] == id_producto:
                    producto_encontrado = p
                    break
                

            if producto_encontrado is not None:
                encabezados = f"\033[1m| {'ID':<15} | {'DESCRIPCIÓN':<15} | {'PRECIO':<15} | {'STOCK':<15} |\033[0m"
                separador = "\033[1;34m" + "*" * 75 + "\033[0m" 

                print(separador)
                print(encabezados)
                print(separador)


                
                print(f"| {producto_encontrado['id']:<15} | {producto_encontrado['descripcion']:<15} | {producto_encontrado['precio']:<15} | {producto_encontrado['stock']:<15} |")           
                
                print(separador)
                
                gotoxy(1, 12); confirmacion = input("\033[33m¿Está seguro que quiere eliminar al cliente? (Dígite Si o No): \033[0m").lower()
                if confirmacion == 'si':
                # Eliminar el cliente de la lista de clientes
                    productos.remove(producto_encontrado)
                            # Guardar los clientes restantes en el archivo JSON
                    json_file.save(productos)
                    gotoxy(1,14);print("\033[32m producto eliminado con éxito ✅\033[0m")
                else:
                    gotoxy(1,14);print("\033[32mEl producto no ha sido eliminado.\033[0m")
            else:
                    gotoxy(1,14);print("\033[31m producto no encontrado, ingrese un ID correcto.\033[0m")
            gotoxy(1, 16)
            decision = input("\033[32m¿Desea eliminar otro producto? (si/no): \033[0m").strip().lower()
            if decision == 'no':
                break

           
    def consult(self):

        
        while True:
            borrarPantalla()
            # Consultar información de un producto
            gotoxy(0, 1)
            print("\033[1;36m" + "█" * 90)  # Línea verde
            gotoxy(1, 2)
            print("██" + " " * 34 + "Mostrar producto" + " " * 37 + "██")
            gotoxy(2, 1)
            print("\033[1;36m" + "█" * 90)  # Línea verde
            json_file = JsonFile(path + '/archivos/products.json')
            productos = json_file.read()

            gotoxy(1,4);id_producto = int(input("Ingrese el ID del producto a consultar: "))
            
            producto_encontrado = None
            for p in productos:
                if p["id"] == id_producto:
                    producto_encontrado = p
                    break
            
            if producto_encontrado is not None:
                encabezados = f"\033[1m| {'ID':<15} | {'DESCRIPCIÓN':<15} | {'PRECIO':<15} | {'STOCK':<15} |\033[0m"
                separador = "\033[1;34m" + "*" * 75 + "\033[0m" 

                print(separador)
                print(encabezados)
                print(separador)


                
                print(f"| {producto_encontrado['id']:<15} | {producto_encontrado['descripcion']:<15} | {producto_encontrado['precio']:<15} | {producto_encontrado['stock']:<15} |")           
                
                print(separador)                       
            else:
                    gotoxy(1,14);print("\033[31m producto no encontrado, ingrese un ID correcto.\033[0m")
            gotoxy(1, 16)
            decision = input("\033[32m¿Desea consultar otro producto? (si/no): \033[0m").strip().lower()
            if decision == 'no':
                break

    def all_consult(self):
        # Borrar pantalla
        borrarPantalla()
        
        # Leer los productos del archivo JSON
        json_file = JsonFile(path + '/archivos/products.json')
        productos = json_file.read()
        
        # Verificar si hay productos
        if not productos:
            print("\033[31mNo hay productos para mostrar.\033[0m")
        else:
            print("\033[1;34m" + "=" * 80 + "\033[0m")
            print(f"\033[1m| {'ID':<15} | {'NOMBRE':<15} | {'PRECIO':<15} |{'STOCK':<15} |\033[0m")
            print("\033[1;34m" + "=" * 80 + "\033[0m")
            
            # Mostrar información de cada producto
            for producto in productos:
                print(f"| {producto['id']:<15} | {producto['descripcion']:<15} | {producto['precio']:<15} | {producto['stock']:<15} |")
                print("\033[1;34m" + "=" * 80 + "\033[0m")
        
        # Esperar a que el usuario presione una tecla para regresar al menú
        input("\033[32mPresione una tecla para regresar al menú.\033[0m")



class CrudSales(ICrud):
    def create(self):
        # cabecera de la venta
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Registro de Venta")
        gotoxy(17,3);print(blue_color+Company.get_business_name())
        gotoxy(5,4);print(f"Factura#:F0999999 {' '*3} Fecha:{datetime.datetime.now()}")
        gotoxy(66,4);print("Subtotal:")
        gotoxy(66,5);print("Decuento:")
        gotoxy(66,6);print("Iva     :")
        gotoxy(66,7);print("Total   :")
        gotoxy(15,6);print("Cedula:")
        
        dni=validar.solo_numeros("Error: Solo numeros",23,6)
        json_file = JsonFile(path+'/archivos/clients.json')
        client = json_file.find("dni",dni)
        if not client:
            gotoxy(35,6);print("Cliente no existe")
            return
        client = client[0]
        cli = RegularClient(client["nombre"],client["apellido"], client["dni"], card=True) 
        sale = Sale(cli)
        gotoxy(35,6);print(cli.fullName())
        gotoxy(2,8);print(green_color+"*"*90+reset_color) 
        gotoxy(5,9);print(purple_color+"Linea") 
        gotoxy(12,9);print("Id_Articulo") 
        gotoxy(24,9);print("Descripcion") 
        gotoxy(38,9);print("Precio") 
        gotoxy(48,9);print("Cantidad") 
        gotoxy(58,9);print("Subtotal") 
        gotoxy(70,9);print("n->Terminar Venta)"+reset_color)
        # detalle de la venta
        follow ="s"

        line=1
        while follow.lower()=="s":
            gotoxy(7,9+line);print(line)
            gotoxy(15,9+line);
            id=int(validar.solo_numeros("Error: Solo numeros",15,9+line))
            json_file = JsonFile(path+'/archivos/products.json')
            prods = json_file.find("id",id)
            if not prods:
                gotoxy(24,9+line);print("Producto no existe")
                time.sleep(1)
                gotoxy(24,9+line);print(" "*20)
            else:    
                prods = prods[0]
                product = Product(prods["id"],prods["descripcion"],prods["precio"],prods["stock"])
                gotoxy(24,9+line);print(product.descrip)
                gotoxy(38,9+line);print(product.preci)
                gotoxy(49,9+line);qyt=int(validar.solo_numeros("Error:Solo numeros",49,9+line))
                gotoxy(59,9+line);print(product.preci*qyt)
                sale.add_detail(product,qyt)
                gotoxy(76,4);print(round(sale.subtotal,2))
                gotoxy(76,5);print(round(sale.discount,2))
                gotoxy(76,6);print(round(sale.iva,2))
                gotoxy(76,7);print(round(sale.total,2))
                gotoxy(74,9+line);follow=input() or "s"  
                gotoxy(76,9+line);print(green_color+"✔"+reset_color)  
                line += 1
        gotoxy(15,9+line);print(red_color+"Esta seguro de grabar la venta(s/n):")
        gotoxy(54,9+line);procesar = input().lower()
        if procesar == "s":
            gotoxy(15,10+line);print("😊 Venta Grabada satisfactoriamente 😊"+reset_color)
            # print(sale.getJson())  
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            ult_invoices = invoices[-1]["factura"]+1
            data = sale.getJson()
            data["factura"]=ult_invoices
            invoices.append(data)
            json_file = JsonFile(path+'/archivos/invoices.json')
            json_file.save(invoices)
        else:
            gotoxy(20,10+line);print("🤣 Venta Cancelada 🤣"+reset_color)    
        time.sleep(2)    
    
    def update(self):
        while True:
            # Función para actualizar una venta existente
            borrarPantalla()
            
            # Solicitar el número de factura a actualizar
            gotoxy(2, 1)
            print("\033[1;36m" + "█" * 90)
            gotoxy(2, 2)
            print("██" + " " * 34 + "Actualizar Venta" + " " * 36 + "██")
            gotoxy(2, 4)
            num_factura = input("\033[32mIngrese el número de factura a actualizar: \033[0m")
            
            if not num_factura.isdigit():
                gotoxy(2, 6)
                print("\033[31mError: Ingrese un número de factura válido.\033[0m")
                time.sleep(2)
                return
            
            num_factura = int(num_factura)
            json_file = JsonFile(path + '/archivos/invoices.json')
            invoices = json_file.read()
            
            # Buscar la venta con el número de factura proporcionado
            venta_encontrada = None
            for invoice in invoices:
                if invoice["factura"] == num_factura:
                    venta_encontrada = invoice
                    break
            
            if not venta_encontrada:
                gotoxy(2, 6)
                print("\033[31mNo se encontró una venta con ese número de factura.\033[0m")
                time.sleep(2)
                return
            
            # Mostrar la venta encontrada y pedir cambios
            print("\033[1;36m" + "█" * 90 + "\033[0m")
            print("\033[1;36m" + "██" + " " * 35 + "Venta Detalles" + " " * 37 + "██" + "\033[0m")
            print("\033[1;36m" + "█" * 90 + "\033[0m")
            print(f"\033[32mFactura #: {venta_encontrada['factura']}     Fecha: {venta_encontrada['Fecha']}    Cliente: {venta_encontrada['cliente']}\033[0m")
            print("\033[1;34m" + "-" * 90 + "\033[0m")
            print(f"\033[32mSubtotal: {venta_encontrada['subtotal']}     Descuento: {venta_encontrada['descuento']}     IVA: {venta_encontrada['iva']}     Total: {venta_encontrada['total']}\033[0m")
            print("\033[1;34m" + "-" * 90 + "\033[0m")
        
        # Mostrar encabezado para los detalles
            print("\033[1m| {:<20} | {:<10} | {:<10} | {:<10} |\033[0m".format(
                "Producto", "Precio", "Cantidad", "Subtotal"
            ))
            print("\033[1;34m" + "-" * 66 + "\033[0m")
        
            for detalle in venta_encontrada['detalle']:
                producto = detalle['poducto']
                precio = detalle['precio']
                cantidad = detalle['cantidad']
                subtotal = precio * cantidad
                print(f"| {producto:<20} | {precio:<10} | {cantidad:<10} | {subtotal:<10} |")
        # Separador al final
            print("\033[1;34m" + "-" * 66 + "\033[0m")
        
        # Esperar a que el usuario presione una tecla para continu
            # Solicitar cambios
            gotoxy(2, 14)
            nuevo_cliente = gotoxy(1,18);input("\033[32mIngrese el nuevo nombre del cliente (o presione Enter para mantener el actual): \033[0m").strip()
            nueva_fecha = gotoxy(1,20);input("\033[32mIngrese la nueva fecha (YYYY-MM-DD) (o presione Enter para mantener la actual): \033[0m").strip()
            nuevo_subtotal = gotoxy(1,22);input("\033[32mIngrese el nuevo subtotal (o presione Enter para mantener el actual): \033[0m").strip()
            nuevo_descuento = gotoxy(1,24);input("\033[32mIngrese el nuevo descuento (o presione Enter para mantener el actual): \033[0m").strip()
            nuevo_iva = gotoxy(1,26);input("\033[32mIngrese el nuevo IVA (o presione Enter para mantener el actual): \033[0m").strip()
            nuevo_total = gotoxy(1,28);input("\033[32mIngrese el nuevo total (o presione Enter para mantener el actual): \033[0m").strip()
            
            # Actualizar los detalles de la venta si se ingresaron valores nuevos
            if nuevo_cliente:
                venta_encontrada['cliente'] = nuevo_cliente
            if nueva_fecha:
                venta_encontrada['Fecha'] = nueva_fecha
            if nuevo_subtotal:
                venta_encontrada['subtotal'] = float(nuevo_subtotal)
            if nuevo_descuento:
                venta_encontrada['descuento'] = float(nuevo_descuento)
            if nuevo_iva:
                venta_encontrada['iva'] = float(nuevo_iva)
            if nuevo_total:
                venta_encontrada['total'] = float(nuevo_total)
            
            # Guardar los cambios en el archivo JSON
            json_file.save(invoices)
            
            gotoxy(2, 20)
            print("\033[32mVenta actualizada con éxito.\033[0m")

            decision = input("\033[32m¿Desea actualizar otro producto? (si/no): \033[0m").strip().lower()
            if decision == 'no':
                break
            
        
    def delete(self):
        while True:
            # Limpiar pantalla
            borrarPantalla()

            # Solicitar el número de factura a eliminar
            gotoxy(2, 1)
            print("\033[1;36m" + "█" * 90)
            gotoxy(2, 2)
            print("██" + " " * 34 + "Eliminar Venta" + " " * 34 + "██")
            gotoxy(2, 4)
            num_factura = input("\033[32mIngrese el número de factura a eliminar: \033[0m")

            # Validar número de factura
            if not num_factura.isdigit():
                gotoxy(2, 6)
                print("\033[31mError: Ingrese un número de factura válido.\033[0m")
                time.sleep(2)
                return

            num_factura = int(num_factura)
            json_file = JsonFile(path + '/archivos/invoices.json')
            invoices = json_file.read()

            # Buscar la venta con el número de factura proporcionado
            venta_encontrada = None
            for invoice in invoices:
                if invoice["factura"] == num_factura:
                    venta_encontrada = invoice
                    break

            # Verificar si la venta existe
            if venta_encontrada is None:
                gotoxy(2, 6)
                print("\033[31mNo se encontró una venta con ese número de factura.\033[0m")
                time.sleep(2)
                return

            # Mostrar información de la venta encontrada
            gotoxy(2, 8)
            print("\033[32mVenta encontrada:")
            print(f"Factura: {venta_encontrada['factura']} - Fecha: {venta_encontrada['Fecha']} - Cliente: {venta_encontrada['cliente']}\033[0m")
            print("\033[34m" + "=" * 80 + "\033[0m")

            # Mostrar detalles de la venta
            print("\033[32mDetalle de la venta:\033[0m")
            print("\033[34m" + "=" * 80 + "\033[0m")
            for detalle in venta_encontrada["detalle"]:
                print(f"Producto: {detalle['poducto']} - Precio: {detalle['precio']} - Cantidad: {detalle['cantidad']}")

            print("\033[34m" + "=" * 80 + "\033[0m")

            # Preguntar si se quiere eliminar la venta completa o un producto específico
            decision = input("\033[33m¿Desea eliminar la venta completa o un producto específico? (venta/producto): \033[0m").strip().lower()

            if decision == 'venta':
                # Eliminar la venta completa
                invoices.remove(venta_encontrada)
                json_file.save(invoices)
                gotoxy(1, 18)
                print("\033[32mVenta eliminada con éxito.✅\033[0m")

            elif decision == 'producto':
                # Eliminar un producto específico de la venta
                producto_id = int(input("\033[32mIngrese el ID del producto a eliminar: \033[0m"))
                detalle_encontrado = None

                # Buscar el producto dentro del detalle de la venta
                for detalle in venta_encontrada["detalle"]:
                    if detalle["poducto"] == producto_id:
                        detalle_encontrado = detalle
                        break
                
                if detalle_encontrado:
                    venta_encontrada["detalle"].remove(detalle_encontrado)

                    # Si no hay más productos, eliminar la venta completa
                    if len(venta_encontrada["detalle"]) == 0:
                        invoices.remove(venta_encontrada)
                    json_file.save(invoices)
                    gotoxy(1, 18)
                    print("\033[32mProducto eliminado con éxito.✅\033[0m")
                else:
                    gotoxy(1, 18)
                    print("\033[31mProducto no encontrado. Ingrese un ID correcto.\033[0m")

            else:
                gotoxy(1, 10)
                print("\033[31mOpción no válida. Ingrese 'venta' o 'producto'.\033[0m")
            decision = input("\033[32m¿Desea eliminar otro producto? (si/no): \033[0m").strip().lower()
            if decision == 'no':
                break
           


    
    def consult(self):
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2, 1)
        print("\033[1;36m" + "█" * 90)
        gotoxy(2, 2)
        print("██" + " " * 34 + "Consulta de Venta" + " " * 34 + "██")
        gotoxy(2, 4)
        
        # Solicitar el número de factura a consultar
        num_factura = input("\033[32mIngrese el número de factura a consultar: \033[0m")
        
        if not num_factura.isdigit():
            gotoxy(2, 6)
            print("\033[31mError: Ingrese un número de factura válido.\033[0m")
            time.sleep(2)
            return
        
        num_factura = int(num_factura)
        json_file = JsonFile(path + '/archivos/invoices.json')
        invoices = json_file.read()
        
        # Buscar la venta con el número de factura proporcionado
        venta_encontrada = None
        for invoice in invoices:
            if invoice["factura"] == num_factura:
                venta_encontrada = invoice
                break
        
        # Mostrar la información de la venta si se encuentra
        if venta_encontrada:
            borrarPantalla()
            print("\033[1;36m" + "█" * 90 + "\033[0m")
            print("\033[1;36m" + "██" + " " * 35 + "Venta Detalles" + " " * 37 + "██" + "\033[0m")
            print("\033[1;36m" + "█" * 90 + "\033[0m")
            print(f"\033[32mFactura #: {venta_encontrada['factura']}     Fecha: {venta_encontrada['Fecha']}    Cliente: {venta_encontrada['cliente']}\033[0m")
            print("\033[1;34m" + "-" * 90 + "\033[0m")
            print(f"\033[32mSubtotal: {venta_encontrada['subtotal']}     Descuento: {venta_encontrada['descuento']}     IVA: {venta_encontrada['iva']}     Total: {venta_encontrada['total']}\033[0m")
            print("\033[1;34m" + "-" * 90 + "\033[0m")
            
            # Mostrar los detalles de los productos en formato de tabla
            
            print("\033[1;34m" + "-" * 90 + "\033[0m")
            
            print("\033[1m{:15s} {:10s} {:10s}\033[0m".format("Producto", "Precio", "Cantidad"))
           
            print("\033[1;34m" + "-" * 90 + "\033[0m")
            
            for detalle in venta_encontrada["detalle"]:
                
                print("{:15s} {:10.2f} {:10}".format(
                    detalle["poducto"],
                    detalle["precio"],
                    detalle["cantidad"]
                ))
            
            # Dar opción al usuario para continuar
            gotoxy(2, 20)
            input("\033[32mPresione cualquier tecla para continuar...\033[0m")
        else:
            gotoxy(2, 6)
            print("\033[31mNo se encontró una venta con ese número de factura.\033[0m")
            time.sleep(2)
    
    def all_consult(self):
        # Borrar pantalla
        borrarPantalla()
        
        # Leer las ventas del archivo JSON
        json_file = JsonFile(path + '/archivos/invoices.json')
        ventas = json_file.read()
        
        # Verificar si hay ventas
        if not ventas:
            gotoxy(2, 2)
            print("\033[31mNo hay ventas para mostrar.\033[0m")
        else:
            # Mostrar encabezados de la tabla
            gotoxy(2, 2)
            print("\033[1;34m" + "=" * 70 + "\033[0m")
            gotoxy(2, 3)
            print(f"\033[1m| {'Factura':<10} | {'Fecha':<12} | {'Cliente':<20} | {'Subtotal':<10} | {'Total':<10} | {'Detalle':<10} |\033[0m")
            gotoxy(2, 4)
            print("\033[1;34m" + "=" * 70 + "\033[0m")
            
            # Mostrar información de cada venta
            for venta in ventas:
                # Formatear los detalles de los productos en la venta
                detalles = ", ".join([f"{detalle['poducto']} ({detalle['cantidad']} x {detalle['precio']})" for detalle in venta['detalle']])
                
                # Mostrar la información de la factura en la tabla
                gotoxy(2, 5)
                print(f"| {venta['factura']:<10} | {venta['Fecha']:<12} | {venta['cliente']:<20} | {venta['subtotal']:<10} | {venta['total']:<10} | {detalles:<20} |")
                print("\033[1;34m" + "-" * 70 + "\033[0m")
            
            # Esperar a que el usuario presione una tecla para regresar al menú
            gotoxy(2, 6)
            input("\033[32mPresione una tecla para regresar al menú.\033[0m")


# Menu Proceso Principal
opc = ''
while opc != '5': 
    borrarPantalla()
    menu_main = Menu("Menu Facturación", ["1) Clientes", "2) Productos", "3) Ventas", "4) Consulta General", "5) Salir"], 2, 2)
    opc = menu_main.menu()
    
    if opc == "1":
        crud_clients = CrudClients(JsonFile)
        opc1 = ''
        while opc1 != '5':
            borrarPantalla()
            menu_clients = Menu("Menú Clientes", ["1) Ingresar", "2) Actualizar", "3) Eliminar", "4) Consultar", "5) Salir"], 2, 2)
            opc1 = menu_clients.menu()
            if opc1 == "1":
                crud_clients.create()
            elif opc1 == "2":
                crud_clients.update()
            elif opc1 == "3":
                crud_clients.delete()
            elif opc1 == "4":
                crud_clients.consult()
                
    elif opc == "2":
        crud_products = CrudProducts(JsonFile)
        opc2 = ''
        while opc2 != '5':
            borrarPantalla()
            menu_products = Menu("Menú Productos", ["1) Ingresar", "2) Actualizar", "3) Eliminar", "4) Consultar", "5) Salir"], 2, 2)
            opc2 = menu_products.menu()
            if opc2 == "1":
                crud_products.create()
            elif opc2 == "2":
                crud_products.update()
            elif opc2 == "3":
                crud_products.delete()
            elif opc2 == "4":
                crud_products.consult()
                
    elif opc == "3":
        opc3 = ''
        while opc3 != '5':
            borrarPantalla()
            sales = CrudSales()
            menu_sales = Menu("Menú Ventas", ["1) Registro Venta", "2) Consultar", "3) Modificar", "4) Eliminar", "5) Salir"], 2, 2)
            opc3 = menu_sales.menu()
            if opc3 == "1":
                sales.create()
            elif opc3 == "2":
                sales.consult()
            elif opc3 == "3":
                sales.update()
            elif opc3 == "4":
                sales.delete()
                
    elif opc == "4":
        
        borrarPantalla()
        menu_consulta = Menu("Consulta General", ["1) Consultar Clientes", "2) Consultar Productos", "3) Consultar Ventas", "4) Regresar al menú principal"], 2, 2)
        consulta_opc = menu_consulta.menu()
        
        if consulta_opc == "1":
            crud_clients = CrudClients(JsonFile)
            crud_clients.all_consult()  # Llamar a la función de consulta de clientes
        
        elif consulta_opc == "2":
            crud_products = CrudProducts(JsonFile)
            crud_products.all_consult()  # Llamar a la función de consulta de productos
        
        elif consulta_opc == "3":
            sales = CrudSales()
            sales.all_consult()  # Llamar a la función de consulta de ventas
        
    print("Regresando al menú principal...")
    time.sleep(2)

borrarPantalla()
input("Presione una tecla para salir...")
borrarPantalla()


