import cx_Oracle
from products import fetch_products, insert_products

cx_Oracle.init_oracle_client(lib_dir="/Users/esteban/Downloads/instantclient_19_8")

username = 'ESTEBAN_ARCE'
password = '123456'
host = '54.213.164.78'
port = '1521'

connection = cx_Oracle.connect(username, password, host + ':' + port + '/')

###################################################################################################
## Funciones universales.
###################################################################################################

#Esta funcion valida que los valores en el input sean solo numeros.
def validate_number_input():
    while True:
        value = input()
        if value.isdigit():
            return int(value)
        print("Valor invalido. Por favor ingrese un numero.")

###################################################################################################
## Estas funciones son para el primer menu, donde se inicia la sesion.

# Al llamar esta funcion despliega el menu de inicio de sesion.
def login_menu():
    login_menu = '''
    --- Inicio de sesión Cafetería Cernícalo ---

    1. Iniciar Sesión
    2. Crear Usuario
    3. Ver Usuarios
    4. Salir
    '''
    print(login_menu)
    print('Ingrese una opción (1-4): ')
    choice = validate_number_input()
    if 1 <= choice <= 4:
        return choice
    print("Opcion invalida. Favor intenta nuevamente.")

# Aquí se realiza el logeo, de ser exitoso devuelve una booleana (True) que se usara más abajo.
def login(users, current_user):
    print('--- Inicio de sesion Cafeteria Cernícalo ---\n')
    while True:
        print("Ingrese Usuario: ")
        username = input()
        print("Ingrese Contraseña: ")
        password = input()

        login_successful = False

        for user in users:
            if user["username"] == username and user["password"] == password:
                cashier = {"username": username, "password": password}
                current_user.append(cashier)

                login_successful = True
                break

        if login_successful:
            print('*** Inicio de Sesión exitoso! ***\n')
            print('Bienvenido', current_user[0]['username'],'!')
            return True
        else:
            print('*** Usuario o contraseña invalido/s ****')
            return

# Esta funcion permite crear nuevos usuarios para que puedan acceder a la comanda. Para poder registrar nuevos usuarios, se preguntara primero por unas credenciales especiales -en este caso estan hardcodeas siendo username: 'admin' y password: 'pass', si se ingresan estas credenciales se podrá crear más usuarios, de lo contrario se devolvera al menu anterior mostrando un mensaje.
def create_user(users):
    print('**** Solo el administrador puede crear usuarios ****\n')
    print("Ingrese Usuario: ")
    username = input()
    print("Ingrese Contraseña: ")
    password = input()

    if username == 'admin' and password == 'pass':
        print('*** Creando nuevo usuario ***\n')
        print('Ingrese nombre de usuario a crear: ')
        username = input()
        print('Ingrese contraseña: ')
        password = input()
        new_user = {'username': username, 'password': password}
        users.append(new_user)
        print('--*** Usuario creado con exito! ***--')
    else: 
        print('**** Usuario o contraseña invalidos para crear usuarios ****')
        return

# Muestra los usuarios registrados hasta el momento, de no haber da un aviso.
def show_users(users):
    print('**** Listado de Usuarios ****\n')

    if not users:
        print('--- No hay usurios registrados ---')
    else:
        for user in users:
            print(f"Nombre de Usuario: {user['username']}")
            print('----------------------------------------')

###################################################################################################
## Esta funciones son las necesarias para hacer correr el menu de la comanda POS.
###################################################################################################

#  Esta funcion crea un producto y lo agrega a la lista products como diccionario.
def create_product(products, connection):
    print('*** Creando un nuevo producto! ***\n')

    print('Ingresa el codigo del producto: ')
    codigo = validate_number_input()
    print('Ingresa el nombre del producto: ')
    nombre = input()
    print('Ingresa la categoria del producto: ')
    categoria = input()
    print('Ingresa el stock del producto: ')
    stock = validate_number_input()
    print('Ingresa el precio del producto: ')
    precio = validate_number_input()

    product_info = {
        "codigo": codigo,
        "nombre": nombre,
        "categoria": categoria,
        "stock": stock,
        "precio": precio
    }

    products.append(product_info)
    print('*** Producto creado con exito! ***')

    insert_products(connection, products)

    print('Deseas crear otro producto? (Y/N): ')
    choice = input()
    if choice.lower() == "y":
        create_product(products)
    elif choice.lower() == "n":
        return
    else:
        print('Opcion invalida! Favor escoja una nuevamente.')

# Muestra los productos y de no haber ninguno lo informa.
def show_products(products):
    print('*** Listado de Productos ***\n')
    if not products:
        print('No se han ingresado productos.')
    else:
        for product in products:
            print(f"Codigo Producto: {product['codigo']}")
            print(f"Nombre Producto: {product['nombre']}")
            print(f"Categoria Producto: {product['categoria']}")
            print(f"Stock Producto: {product['stock']}")
            print(f"Precio Producto: {product['precio']}")
            print('--------------------------------')

# Es igual a la de crear productos, crea un usuario como diccionario y lo agrega a la lista customers.
def create_customer(customers):
    print('*** Creando un nuevo cliente ***\n')

    print('Ingresa el nombre del cliente: ')
    nombre = input()
    print('Ingresa el apellido del cliente: ')
    apellido= input()
    print('Ingresa el RUT del cliente: ')
    rut = validate_number_input()
    print('Ingresa el correo del cliente: ')
    email = input()
    print('Ingresa el numero de telefono del cliente: ')
    telefono = validate_number_input()

    customer_info = {
        "nombre": nombre,
        "apellido": apellido,
        "rut": rut,
        "email": email,
        "telefono": telefono
    }

    customers.append(customer_info)
    print('Cliente creado existosamente!')

    print('Deseas crear otro cliente? (Y/N): ')
    choice = input()
    if choice.lower() == "y":
        create_customer(customers)
    elif choice.lower() == "n":
        return
    else:
        print('Opcion invalida! Favor escoja nuevamente.')

# Muestra los usuarios y de no haber ninguno da un aviso.
def show_customers(customers):
    print('*** Listado de clientes ***\n')
    if not customers:
        print('No se han registrados clientes.')
    else:    
        for customer in customers:
            full_name = f"{customer['nombre']} {customer['apellido']}"
            print(f"Nombre Completo: {full_name}")
            print(f"RUT Cliente: {customer['rut']}")
            print(f"Correo Cliente: {customer['email']}")
            print(f"Telefono Cliente: {customer['telefono']}")
            print('----------------------------------------')

# Esta funcion es la que hará la venta, pide el rut del cliente y lo busca en la lista, de no existir preguntará si deseas crearlo -si la opcion es no, volvera al menu anterior- al crearlo la venta prosigue, crea una boleta como diccionario y la guarda en la lista daily_sales ademas de actualizar el stock e informar si la cantidad saliente es mayor a la disponible.
def sale(customers, products, daily_sales):
    print('*** Generando una venta ***\n')

    print('Ingrese RUT del cliente: ')
    rut = validate_number_input()

    customer = None
    for c in customers:
        if c["rut"] == rut:
            customer = c
            break

    if customer is None:
        while True:
            print('Cliente no encontrado. Desea crearlo?: (Y/N)')
            choice = input()
            if choice.lower() == 'y':
                create_customer(customers)
                # print(customers[-1]) si descomentan esta linea pueden ver en la terminal por qué en la linea de abajo se usa "-1" para acceder a la variable customers.
                customer = customers[-1]
                break
            elif choice.lower() == 'n':
                print('--- Volviendo al menu principal ---')
                return False
            else:
                print('Opcion invalida! Favor escoja una nuevamente.')
                continue
    
    print('Ingrese el tipo de pago: ')
    payment_method = input()

    boleta = {
        "cliente": customer,
        "productos": {},
        "tipo_pago": payment_method
    }

    while True:
        print('Ingrese el codigo del producto (Ingrese "0" para finalizar la venta): ')
        codigo_producto = validate_number_input()

        if codigo_producto == 0:
            break

        product = None
        for p in products:
            if p['codigo'] == codigo_producto:
                product = p
                break

        if product is None:
            print('Codigo de producto invalido o no existente. Favor intente nuevamente')
            continue
        
        print('Ingrese la cantidad de producto a vender: ')
        cantidad = validate_number_input()

        if cantidad is None:
            print("Cantidad invalida. Favor intente nuevamente.")
            continue

        stock = product["stock"]
        if cantidad > stock:
            print(f"El stock saliente no puede ser mayor al disponible! Stock disponible: {stock}")
            continue

        precio_unitario = product["precio"]
        precio_total = precio_unitario * cantidad

        boleta["productos"][codigo_producto] = {
            "nombre": product["nombre"],
            "categoria": product["categoria"],
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "precio_total": precio_total
        }

        product["stock"] -= cantidad

    daily_sales.append(boleta)
    print('--- Venta registrada exitosamente! ---')

    return

# Muestra la ventas realizadas hasta el momento, de no haber da un aviso
def show_daily_sales(daily_sales):
    print('*** Ventas Diarias ***\n')

    if not daily_sales:
        print('Aun no se han realizado ventas.')
    else: 
        for boleta in daily_sales:
            print("Cliente: ", boleta["cliente"]["nombre"])
            print("RUT: ", boleta["cliente"]["rut"])
            print("Tipo de pago: ", boleta["tipo_pago"])
            print("Productos:")

            for codigo, producto in boleta["productos"].items():
                print("Codigo:", codigo)
                print("Nombre:", producto["nombre"])
                print("Cantidad:", producto["cantidad"])
                print("Precio total:", producto["precio_total"])
                print("---------------")

            total_price = sum(producto["precio_total"] for producto in boleta["productos"].values())
            print("Total a pagar:", total_price)
            print("-------------------------------\n")

    return

# Genera un reporte para el cierre del dia y cierra el programa
def daily_closure(daily_sales, closure_report):
    print('**** Reporte Diario ****\n')
    total_sales = 0
    payment_types = {}
    categories = set()

    for boleta in daily_sales:
        total_sales += sum(producto["precio_total"] for producto in boleta["productos"].values())

        payment_method = boleta["tipo_pago"]
        payment_types[payment_method] = payment_types.get(payment_method, 0) + 1

        for producto in boleta["productos"].values():
            categories.add(producto["categoria"])

    print("Ventas totales del dia:", total_sales)
    print('Cajero del dia:', current_user[0]['username'])
    print("Tipos de pago:")
    for payment_method, count in payment_types.items():
        print(f"- {payment_method}: {count}")
    print("Categorias vendidas:")
    for category in categories:
        print(f"- {category}")

    report = {
        'ventas_totales': total_sales,
        'cajero': current_user[0]['username'],
        'pagos': payment_types,
        'categorias': list(categories)
    }
    closure_report.append(report)

    print('\n')

    exit()

# Este es el menu de la comanda POS, contiene las variables, products, customers y daily_sales. Corre enternamente hasta que se ejecute el cierre diario.
def main_menu():
    running = True

    # products = import_data_from_excel(products_data_file) if products_data_exists else 
    products = []
    products = fetch_products(connection, products)
    
    # customers = import_data_from_excel(customers_data_file) if customers_data_exists else 
    customers = [
            {'nombre': 'Pedro', 'apellido': 'Paramo', 'rut': 1980, 'email': 'pparamo@example.com', 'telefono': 171800200171}, 
            {'nombre': 'Alberto', 'apellido': 'Borges', 'rut': 1190, 'email': 'alberto.borges@example.com', 'telefono': 800360360}
        ]
    
    daily_sales = []

    closure_report = []

    while running:
        menu_options = """
        --- Cafeteria Cernícalo ---

        1. Crear Producto
        2. Mostrar Productos
        3. Crear Cliente
        4. Mostrar Clientes
        5. Venta
        6. Mostrar Ventas 
        7. Cierre Dia
        """
        print(menu_options)
        print("Ingresa una opcion (1-7): ")
        choice = validate_number_input()
        if 1 <= choice <= 7:
            if choice == 1:
                create_product(products, connection)
            elif choice == 2:
                show_products(products)
            elif choice == 3:
                create_customer(customers)
            elif choice == 4:
                show_customers(customers)
            elif choice == 5:
                sale(customers, products, daily_sales)
            elif choice == 6:
                show_daily_sales(daily_sales)
            elif choice == 7:
                daily_closure(daily_sales, closure_report)
        else:
            print("Opcion invalida. Favor intenta nuevamente.")

###################################################################################################
## Con este codigo hacemos correr el menu de inicio de sesion.
running = True

# Aca usando if else shorthand, le damos dos opciones a la variable para ser llenada con data, si users_data_exists es True, se llama a la funcion import_data_from_excel usando como argumento el path al documento que contiene la data de los usuarios, de no ser False, se le asignan valores predeterminados.
# users = import_data_from_excel(users_data_file) if users_data_exists else

users = [{'username': 'benjamin', 'password': 'pass'}, {'username': 'evelyn', 'password': 'pass'}, {'username': 'rafael', 'password': 'pass'}]

current_user = []

while running:
    login_choice = login_menu()

    if login_choice == 1:
        if login(users, current_user):
            #Si el inicio de sesion es exitoso, comenzará a correr el menu POS(productos, clientes, ventas y reportes)
            main_menu()
    elif login_choice == 2:
        create_user(users)
    elif login_choice == 3:
        show_users(users)
    elif login_choice == 4:
        print("Hasta Pronto!")
        running = False
    else:
        print("Por favor ingrese una opcion valida!")
