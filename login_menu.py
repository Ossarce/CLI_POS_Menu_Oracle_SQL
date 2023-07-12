# Importamos Pandas para realizar el importe y el exporte de datos a un excel.
## NOTA: Se debe instalar pandas y openpyxl para que el programa corra
## se puede usar con el siguiente comando en la terminal: pip install pandas y pip install openpyxl.
## si la terminal devuelve algo similar "command not found: pip" agregar un 3 a pip quedando: pip3 install...
import pandas as pd

# Ya conoces esta funcion ajaja.
def validate_number_input():
    while True:
        value = input()
        if value.isdigit():
            return int(value)
        print("valor invalido. Por favor ingrese un numero.")

# Se declara una variable que contiene el nombre(pos_data) y extension(.xlsx) del archivo que almacena los datos.
data_file = "pos_data.xlsx"
# Mas abajo veras para que sirve esta variable.
data_exists = False

# Con un try probaremos primero si es posible leer el archivo dentro de data_file de existir cambiara la variable data_exists a verdadero, de no existir dara un aviso informando que el archivo no ha sido encontrado.
try:
    pd.read_excel(data_file)
    data_exists = True
except FileNotFoundError:
    print(f"Excel '{data_file}' no encontrado.")

# Luego de confirmar que existe el archivo podemos continuar a la importacion usando esta funcion.
# Que nuevamente probara si el archivo -que recibe como argumento- existe. de hacerlo, devolvera como diccionario la informacion. 
def import_data_from_excel(filename, sheet_name):
    try:
        df = pd.read_excel(filename, sheet_name=sheet_name, engine='openpyxl')
        return df.to_dict(orient='records')
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return []
    
# Con esta funcion se pasan dos argumentos uno es la variable(lista con diccionarios) y el archivo donde queremos guardar los datos.
def export_data_to_excel(data, filename, sheet_name):
    df = pd.DataFrame(data)
    writer = pd.ExcelWriter(filename, engine='openpyxl')
    writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)
    df.to_excel(writer, sheet_name=sheet_name, index=False)
    writer.save()


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

def login(users, current_user):
    print('--- Inicio de sesion Cafeteria Cernícalo ---\n')
    while True:
        print('Ingresa usuario: ')
        username = input()
        print('Ingresa contraseña: ')
        password = input()
        
        login_successful = False
        
        for user in users:
            if user['username'] == username and user['password'] == password:
                cashier = {
                    'username' : username,
                    'password' : password
                }
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
        
def create_user(users):
    print('**** Solo el administrador puede crear usuarios ****\n')
    print('Ingrese Usuario: ')
    username = input()
    print('Ingrese Contraseña: ')
    password = input()
    #Para este caso el usuario admin y su contraseña se encuentran hardcodeados pero se puede declarar una variable admin de tipo lista que contenga diccionarios con los usuarios que tengan los permisos suficientes para  la creacion de otros usuarios.
    if username == 'admin' and password == 'pass':
        print('*** Creando nuevo usuario ***\n')
        print('Ingrese nombre de usuario a crear: ')
        username = input()
        print('Ingrese contraseña: ')
        password = input()
        new_user = {'username': username, 'password': password}
        users.append(new_user)
    else: 
        print('**** Usuario o contraseña invalidos para crear usuarios ****')
        return

def show_users(users):
    print('**** Listado de Usuarios ****\n')

    if not users:
        print('--- No hay usurios registrados ---')
    else:
        for user in users:
            print(f"Nombre de Usuario: {user['username']}")
            print('----------------------------------------')

running = True

# Aqui se hace uso de "Un shorthand para escribir If Else": https://www.w3schools.com/python/gloss_python_if_else_shorthand.asp <--- acá hay más info. Lo que hace es revisar si data_exists es True; de serlo se llama a la funcion para importar la data como diccionario y quedarña asignada a la variable users, si  data_exists es False asignara a users la lista con diccionarios que se muestra despues del else. 
users = import_data_from_excel(data_file) if data_exists else [{'username': 'benjamin', 'password': 'pass'}, {'username': 'evelyn', 'password': 'pass'}, {'username': 'rafael', 'password': 'pass'}]

current_user = []

while running:
    login_choice = login_menu()

    if login_choice == 1:
        login(users, current_user)
    elif login_choice == 2:
        create_user(users)
        # Como mencionaste anteriormente al realizar el cierre del día se guarden los datos en un excel pero en el caso de los usuarios lo mejor seria que una vez se agregue un usuario nuevo cambie los datos del excel.
        export_data_to_excel(users ,data_file, 'Users')
    elif login_choice == 3:
        show_users(users)
    elif login_choice == 4:
        print('Toodles!')
        running = False
    else:
        print('Come on Mate! Choose a valid option!')

