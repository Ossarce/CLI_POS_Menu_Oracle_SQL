
def fetch_customers(connection, customers):
    cursor = connection.cursor()

    query = 'SELECT * FROM CUSTOMERS'
    cursor.execute(query)
    for row in cursor.fetchall():
        print(row)

        customer = {
            'customer_id': row[0],
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

    existing_query = 'SELECT COUNT(*) FROM CUSTOMERS WHERE rut = :rut'
    cursor.execute(existing_query, rut=customer['rut'])
    count = cursor.fetchone()[0]

    if count == 0:
        insert_query = 'INSERT INTO CUSTOMERS (nombre, apellido, rut, email, telefono) ' \
                       'VALUES (:nombre, :apellido, :rut, :email, :telefono)'
        cursor.execute(insert_query, nombre=customer['nombre'], apellido=customer['apellido'], rut=customer['rut'],
                       email=customer['email'], telefono=customer['telefono'])
        
        connection.commit()

        # Fetch the generated customer_id using a separate query
        fetch_customer_id_query = 'SELECT customer_id FROM CUSTOMERS WHERE rut = :rut'
        cursor.execute(fetch_customer_id_query, rut=customer['rut'])
        generated_customer_id = cursor.fetchone()[0]

        print('El cliente:', customer['nombre'] + customer['apellido'], 'ha sido agregado a la base de datos.')
    else:
        print('El cliente:', customer['nombre'] + customer['apellido'], 'ya existe en la base de datos.')
        generated_customer_id = None

    cursor.close()

    return generated_customer_id





# def get_customer_id(connection, rut):
#     cursor = connection.cursor()
#     query = "SELECT customer_id FROM customers WHERE rut = :rut"
#     cursor.execute(query, rut=rut)
#     row = cursor.fetchone()
#     if row:
#         return row[0]
#     else:
#         return None
