def fetch_products(connection, products):
    cursor = connection.cursor()

    query = 'SELECT * FROM PRODUCTS'
    cursor.execute(query)
    for row in cursor.fetchall():
        print(row)

        product = {
            'codigo': row[0],
            'nombre': row[1],
            'categoria': row[2],
            'stock': row[3],
            'precio': row[4],
        }

        products.append(product)

    cursor.close()

    return products

def insert_products(connection, products):
    cursor = connection.cursor()

    for product in products:
        existing_query = "SELECT COUNT(*) FROM PRODUCTS WHERE CODIGO = :codigo"
        cursor.execute(existing_query, codigo =product['codigo'])
        count = cursor.fetchone()[0]

        if count == 0:
            insert_query = "INSERT INTO PRODUCTS (codigo, nombre, categoria, stock, precio) " \
                           "VALUES (:codigo, :nombre, :categoria, :stock, :precio)"
            cursor.execute(insert_query, product)
            print("El producto:", product['nombre'], 'ha sido agregado a la base de datos.')
        else:
            print("El producto:", product['nombre'], 'ya existe en la base de datos.')

    connection.commit()

    cursor.close()

def update_product_stock(connection, product_code, new_stock):
    cursor = connection.cursor()

    update_query = "UPDATE PRODUCTS SET stock = :new_stock WHERE codigo = :product_code"
    cursor.execute(update_query, new_stock=new_stock, product_code=product_code)

    connection.commit()

    cursor.close()