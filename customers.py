
def fetch_customers(connection, customers):
    cursor = connection.cursor()

    query = 'SELECT * FROM CUSTOMERS'
    cursor.execute(query)
    for row in cursor.fetchall():
        print(row)

        customer = {
            'nombre': row[1],
            'apellido': row[2],
            'rut': row[3],
            'email': row[4],
            'telefono': row[5]
        }

        customers.append(customer)

    cursor.close()

    return customers

def insert_customer(connection, customer):
    cursor = connection.cursor()

    existing_query = 'SELECT COUNT(*) FROM CUSTOMERS WHERE nombre = :nombre'
    cursor.execute(existing_query, nombre = customer['nombre'])
    count = cursor.fetchone()[0]

    if count == 0:
        insert_query = 'INSERT INTO CUSTOMERS (nombre, apellido, rut, email, telefono) VALUES (:nombre, :apellido, :rut, :email, :telefono)'

        cursor.execute(insert_query, nombre = customer['nombre'], apellido = customer['apellido'], rut = customer['rut'], email = customer['email'], telefono = customer['telefono'])
        
        print('El cliente:', customer['nombre'] + customer['apellido'], 'ha sido agregado a la base de datos.')
    else:
        print('El cliente:', customer['nombre'] + customer['apellido'], 'ya existe en la base de datos.')
    
    connection.commit()

    cursor.close()