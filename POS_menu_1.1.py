import cx_Oracle
import datetime

from products import fetch_products, insert_product,get_products, update_product_stock
from users import fetch_users, insert_user, get_users
from customers import fetch_customers, insert_customer, get_customers
from sales import insert_receipt, insert_receipt_detail, get_daily_sales
from reports import get_total_sales, get_cashier_username, get_payment_types, get_categories

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
                user_id = user['user_id']
                current_user.append({'user_id': user_id, 'username': username})
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
        new_user = {
            'user_id': None,
            'username': username, 
            'password': password}
        users.append(new_user)
        print('--*** Usuario creado con exito! ***--')

        user_id = insert_user(connection, new_user)
        new_user['user_id'] = user_id
        print(new_user)

    else: 
        print('**** Usuario o contraseña invalidos para crear usuarios ****')
        return

# Muestra los usuarios registrados hasta el momento, de no haber da un aviso.
def show_users(connection):
    users = get_users(connection)
    print('**** Listado de Usuarios ****\n')

    if not users:
        print('--- No hay usuarios registrados ---')
    else:
        for user in users:
            print(f"Nombre de Usuario: {user}")
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
        "product_id": None,
        "codigo": codigo,
        "nombre": nombre,
        "categoria": categoria,
        "stock": stock,
        "precio": precio
    }

    products.append(product_info)
    print('*** Producto creado con exito! ***')

    product_id = insert_product(connection, product_info)
    product_info['product_id'] = product_id

    print('Deseas crear otro producto? (Y/N): ')
    choice = input()
    if choice.lower() == "y":
        create_product(products, connection)
    elif choice.lower() == "n":
        return
    else:
        print('Opcion invalida! Favor escoja una nuevamente.')

# Muestra los productos y de no haber ninguno lo informa.
def show_products(connection):
    products = get_products(connection)

    print('*** Listado de Productos ***\n')
    if not products:
        print('No se han ingresado productos.') 
    else:
        for product in products:
            codigo, nombre, categoria, stock, precio = product
            print(f"Codigo Producto: {codigo}")
            print(f"Nombre Producto: {nombre}")
            print(f"Categoria Producto: {categoria}")
            print(f"Stock Producto: {stock}")
            print(f"Precio Producto: {precio}")
            print('--------------------------------')

# Es igual a la de crear productos, crea un usuario como diccionario y lo agrega a la lista customers.
def create_customer(customers, connection):
    print('*** Creando un nuevo cliente ***\n')

    print('Ingresa el nombre del cliente: ')
    nombre = input()
    print('Ingresa el apellido del cliente: ')
    apellido = input()
    print('Ingresa el RUT del cliente: ')
    rut = validate_number_input()
    print('Ingresa el correo del cliente: ')
    email = input()
    print('Ingresa el numero de telefono del cliente: ')
    telefono = validate_number_input()

    customer_info = {
        "customer_id": None,
        "nombre": nombre,
        "apellido": apellido,
        "rut": rut,
        "email": email,
        "telefono": telefono
    }

    customers.append(customer_info)
    print('Cliente creado existosamente!')

    customer_id = insert_customer(connection, customer_info)  
    customer_info["customer_id"] = customer_id
    print(customer_info)


    print('Deseas crear otro cliente? (Y/N): ')
    choice = input()
    if choice.lower() == "y":
        create_customer(customers, connection)
    elif choice.lower() == "n":
        return
    else:
        print('Opcion invalida! Favor escoja nuevamente.')

# Muestra los usuarios y de no haber ninguno da un aviso.
def show_customers(connection):
    customers = get_customers(connection)
    print('*** Listado de clientes ***\n')
    if not customers:
        print('No se han registrados clientes.')
    else:
        for customer in customers:
            nombre, apellido, rut, email, telefono = customer
            full_name = f"{nombre} {apellido}"
            print(f"Nombre Completo: {full_name}")
            print(f"RUT Cliente: {rut}")
            print(f"Correo Cliente: {email}")
            print(f"Telefono Cliente: {telefono}")
            print('----------------------------------------')

# Esta funcion es la que hará la venta, pide el rut del cliente y lo busca en la lista, de no existir preguntará si deseas crearlo -si la opcion es no, volvera al menu anterior- al crearlo la venta prosigue, crea una boleta como diccionario y la guarda en la lista daily_sales ademas de actualizar el stock e informar si la cantidad saliente es mayor a la disponible.
def sale(current_user, customers, products, daily_sales, connection):
    print('*** Generando una venta ***\n')

    cursor = connection.cursor()

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
                create_customer(customers, connection)
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

    receipt_date = datetime.date.today().strftime("%d-%m-%Y")

    insert_receipt(connection, customer['customer_id'], current_user[0]['user_id'], payment_method, receipt_date)

    receipt_id = cursor.execute("SELECT receipt_id FROM receipt WHERE ROWNUM = 1 ORDER BY receipt_id DESC").fetchone()[0]

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
        product_id = product['product_id']

        insert_receipt_detail(connection, receipt_id, product_id, cantidad, precio_unitario, precio_total)

        for p in products:
            if p['codigo'] == codigo_producto:
                p['stock'] -= cantidad
                update_product_stock(connection, codigo_producto, p['stock'])
                break

        boleta["productos"][codigo_producto] = {
            "nombre": product["nombre"],
            "categoria": product["categoria"],
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "precio_total": precio_total
        }

    connection.commit()
    cursor.close()

    daily_sales.append(boleta)
    print('--- Venta registrada exitosamente! ---')

# Muestra la ventas realizadas hasta el momento, de no haber da un aviso
def show_daily_sales(connection):
    daily_sales = get_daily_sales(connection)

    print('*** Ventas Diarias ***\n')

    if not daily_sales:
        print('Aun no se han realizado ventas.')
    else:
        for sale in daily_sales:
            receipt_id, customer_name, rut, payment_method, product_id, product_name, quantity, subtotal = sale
            print("Cliente:", customer_name)
            print("RUT:", rut)
            print("Tipo de pago:", payment_method)
            print("Productos:")
            print("Codigo:", product_id)
            print("Nombre:", product_name)
            print("Cantidad:", quantity)
            print("Precio total:", subtotal)
            print("---------------")

        total_price = sum(sale[-1] for sale in daily_sales)
        print("Total a pagar:", total_price)
        print("-------------------------------\n")

# Genera un reporte para el cierre del dia y cierra el programa
def daily_closure(current_user, connection, closure_report):
    cursor = connection.cursor()

    total_sales = get_total_sales(cursor)
    cashier_username = get_cashier_username(current_user)
    payment_types = get_payment_types(cursor)
    categories = get_categories(cursor)

    print("**** Reporte Diario ****\n")
    print("Ventas totales del dia:", total_sales)
    print('Cajero del dia:', cashier_username)
    print("Tipos de pago:")
    for payment_method, count in payment_types.items():
        print(f"- {payment_method}: {count}")
    print("Categorias vendidas:")
    for category in categories:
        print(f"- {category}")

    report = {
        'ventas_totales': total_sales,
        'cajero': cashier_username,
        'pagos': payment_types,
        'categorias': categories
    }
    closure_report.append(report)

    cursor.close()

    print('\n')

    exit()

# Este es el menu de la comanda POS, contiene las variables, products, customers y daily_sales. Corre enternamente hasta que se ejecute el cierre diario.
def main_menu():
    running = True

    products = []
    products = fetch_products(connection, products)
    
    customers = []
    customers = fetch_customers(connection, customers)
    
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
                show_products(connection)
            elif choice == 3:
                create_customer(customers, connection)
            elif choice == 4:
                show_customers(connection)
            elif choice == 5:
                sale(current_user, customers, products, daily_sales, connection)
            elif choice == 6:
                show_daily_sales(connection)
            elif choice == 7:
                daily_closure(current_user, connection, closure_report)
        else:
            print("Opcion invalida. Favor intenta nuevamente.")

###################################################################################################
## Con este codigo hacemos correr el menu de inicio de sesion.
running = True

users = []
users = fetch_users(connection, users)

current_user = []

while running:
    login_choice = login_menu()

    if login_choice == 1:
        if login(users, current_user):
            print(current_user[0]['user_id'])
            main_menu()
    elif login_choice == 2:
        create_user(users)
    elif login_choice == 3:
        show_users(connection)
    elif login_choice == 4:
        print("Hasta Pronto!")
        running = False
    else:
        print("Por favor ingrese una opcion valida!")
