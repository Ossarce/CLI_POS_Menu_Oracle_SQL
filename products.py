def fetch_products(connection, products):
    cursor = connection.cursor()

    query = 'SELECT * FROM PRODUCTS'
    cursor.execute(query)
    for row in cursor.fetchall():
        print(row)

        product = {
            'product_id': row[0],
            'codigo': row[1],
            'nombre': row[2],
            'categoria': row[3],
            'stock': row[4],
            'precio': row[5],
        }

        products.append(product)

    cursor.close()

    return products

def insert_product(connection, product):
    cursor = connection.cursor()

    existing_query = "SELECT COUNT(*) FROM PRODUCTS WHERE CODIGO = :codigo"
    cursor.execute(existing_query, codigo =product['codigo'])
    count = cursor.fetchone()[0]

    if count == 0:
        insert_query = "INSERT INTO PRODUCTS (codigo, nombre, categoria, stock, precio) " \
                        "VALUES (:codigo, :nombre, :categoria, :stock, :precio)"
        cursor.execute(insert_query, product)

        connection.commit()
        fetch_product_id_query = 'SELECT product_id FROM PRODUCTS WHERE codigo = :codigo'
        cursor.execute(fetch_product_id_query, codigo = product['codigo'])
        generated_product_id = cursor.fetchone()[0]
        print("El producto:", product['nombre'], 'ha sido agregado a la base de datos.')
    else:
        print("El producto:", product['nombre'], 'ya existe en la base de datos.')
        generated_product_id = None

    cursor.close()

    return generated_product_id

def get_products(connection):
    cursor = connection.cursor()
    select_query = "SELECT codigo, nombre, categoria, stock, precio FROM products"
    cursor.execute(select_query)
    products = cursor.fetchall()
    return products


def update_product_stock(connection, product_code, new_stock):
    cursor = connection.cursor()

    update_query = "UPDATE PRODUCTS SET stock = :new_stock WHERE codigo = :product_code"
    cursor.execute(update_query, new_stock=new_stock, product_code=product_code)

    connection.commit()

    cursor.close()