# Esta funcion se utiliza para validar que los inputs numericos solo puedan recibir ese tipo de data
# de lo contrario pedirá en loop hasta que se ingrese un valor numerico.
def validate_number_input():
    while True:
        value = input()
        if value.isdigit():
            return int(value)
        print("valor invalido. Por favor ingrese un numero.")

# Funcion que permite logear al trabajador.
def login(users, current_user):
    print('--- Inicio de sesion Cafeteria Cernícalo ---\n')
    while True:
        print('Ingresa usuario: ')
        username = input()
        print('Ingresa contraseeña: ')
        password = input()
        if username in users and users[username] == password:
            print("Inicio de sesion existoso!")
            cashier = {'username': username, 'password': password}
            current_user.append(cashier)
            print('----- Bienvenido/a', current_user[0]['username'],'! -----')
            return True
        print("Usuario o contraseña invalida. Por favor intente nuevamente.")

# Funcion de menu principal.
def main_menu():
    while True:
        menu_options = '''
        --- Cafeteria Cernícalo ---

        1. Crear Producto
        2. Mostrar Productos
        3. Crear Cliente
        4. Mostrar Clientes
        5. Venta
        6. Mostrar Ventas
        7. Cierre Dia
        '''
        print(menu_options)
        print('"Ingresa una opcion (1-7): "')
        choice = validate_number_input()
        if 1 <= choice <= 7:
            return choice
        print("Opcion invalida. Favor intenta nuevamente.")

# Aca se crea el producto, cuenta con un loop del que no sale hasta que se confirma que no se agregaran mas productos 
# Ojo que tiene un fallo pues cada vez que sea crea un nuevo producto con la opcion del loop se volvera a preguntar si se desea salir (es mucho mas facil de entender si hacen correr el programa jajaja)
# Se arregló el fallo del loop.
def create_product(products):
    print('*** Creando un nuevo producto! ***')

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

    products[codigo] = product_info
    print('*** Producto creado con exito! ***')

    print('Deseas crear otro producto? (Y/N): ')
    choice = input()
    if choice.lower() == "y":
        create_product(products)
    elif choice.lower() == "n":
        return
    else:
        print('Opcion invalida! Favor escoja una nuevamente.')

# Simplemente consulta los productos y los despliega.
def show_products(products):
    print('*** Listado de Productos ***\n')
    if not products:
        print('No se han ingresado productos.')
    else:
        for codigo, product_info in products.items():
            print(f"Codigo Producto: {codigo}")
            print(f"Nombre Producto: {product_info['nombre']}")
            print(f"Categoria Producto: {product_info['categoria']}")
            print(f"Stock Producto: {product_info['stock']}")
            print(f"Precio Producto: {product_info['precio']}")
            print('--------------------------------')

# Esta funcion crea los usuarios y tiene el mismo problema que la de crear productos 
#YA NO TIENE EL ERROR PERO SE DEJA EL COMENTARIO PARA EL RECUERDO.
def create_customer(customers):
    print('*** Creando un nuevo cliente ***')

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

# Muestra los usuarios ajajaja 
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

# Esta funcion acepta dos parametros consultando si el cliente existe y si el producto es valido, crea una boleta que puede ser consultada con la funcion que sigue.
def sale(customers, products):
    print('*** Generando una venta ***')

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

        product = products.get(codigo_producto)

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

# Esta funcion nos muestra detalles de todas la boletas que han sido generadas en la sesion.
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
            print("-------------------------------")

    return

# Si puede parecerse a la funcion anterior, esta nos mostrará las ventas totales del dia, los tipos de pago y cuantos hubieron de cada uno, asi como las categorias vendidas y cuantas de cada una.
def daily_closure():
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

    return

# Diccionario con usuarios que pueden manejar la comanda.
users = {
    "user": "pass",
    "benjamin": "pass",
    "evelyn": "pass", 
    "rafael": "pass" 
}
current_user = []
# Aquí se da inicio a la sesion de usuario llamando la funcion login con el diccionario users 
# pues como se menciona arriba solo esos usuarios pueden manejar la comanda.
login_successful = login(users, current_user)

if login_successful:
    # Si las credenciales en login(users) son correcta comenzara a correr el programa.
    running = True
    # Estas tres variables comienzan vacias y se encuentran en el scope gobal a fin de poder ser usadas
    # ya sea agregandoles informacion o consultando su contenido por medio de las diversas funciones que encontramos en la primeras lineas de codigo.
    products = {1: 
                {'codigo': 1, 'nombre': 'angelo sosa', 'categoria': 'cafe', 'stock': 6, 'precio': 2000}, 
                2: 
                {'codigo': 2, 'nombre': 'hario mss1', 'categoria': 'molino', 'stock': 3, 'precio': 5000},
                3: 
                {'codigo': 3, 'nombre': 'aeropress go', 'categoria': 'metodos y filtros', 'stock': 5, 'precio': 12000}
                }
    customers = [
        {'nombre': 'Pedro', 'apellido': 'Paramo', 'rut': 1980, 'email': 'pparamo@example.com', 'telefono': 171800200171}, 
        {'nombre': 'Alberto', 'apellido': 'Borges', 'rut': 1190, 'email': 'alberto.borges@example.com', 'telefono': 800360360}
        ]
    daily_sales = []
    
    while running:
        user_choice = main_menu()

        if user_choice == 1:
            create_product(products)
        elif user_choice == 2:
            show_products(products)
        elif user_choice == 3:
            create_customer(customers)
        elif user_choice == 4:
            show_customers(customers)
        elif user_choice == 5:
            sale(customers, products)
        elif user_choice == 6:
            show_daily_sales(daily_sales)
        elif user_choice == 7:
            daily_closure()
            running = False
        else:
            print('Opcion invalida. Favor escoja otra opcion.')
