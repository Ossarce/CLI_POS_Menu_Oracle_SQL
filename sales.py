import datetime

def insert_receipt(connection, customer_id, cashier_id, payment_method, receipt_date):
    cursor = connection.cursor()

    insert_query = "INSERT INTO receipt (customer_id, cashier_id, payment_method, receipt_date) " \
                   "VALUES (:customer_id, :cashier_id, :payment_method, TO_DATE(:receipt_date, 'DD-MM-YYYY'))"
    receipt_info = {
        "customer_id": customer_id,
        "cashier_id": cashier_id,
        "payment_method": payment_method,
        "receipt_date": receipt_date
    }
    cursor.execute(insert_query, receipt_info)

    connection.commit()
    cursor.close()
    print('Boleta registrada correctamente en la Base de datos!')

def insert_receipt_detail(connection, receipt_id, product_id, quantity, price, subtotal):
    cursor = connection.cursor()

    insert_query = "INSERT INTO receipt_detail (receipt_id, product_id, quantity, price, subtotal) " \
                   "VALUES (:receipt_id, :product_id, :quantity, :price, :subtotal)"
    receipt_detail = {
        "receipt_id": receipt_id,
        "product_id": product_id,
        "quantity": quantity,
        "price": price,
        "subtotal": subtotal
    }
    cursor.execute(insert_query, receipt_detail)


    update_query = "UPDATE receipt " \
                   "SET total_amount = (SELECT SUM(subtotal) FROM receipt_detail WHERE receipt_id = :receipt_id) " \
                   "WHERE receipt_id = :receipt_id"
    cursor.execute(update_query, {"receipt_id": receipt_id})

    connection.commit()
    cursor.close()
    print('Detalles de la boleta ingresados correctamente en la Base de datos!')


def get_daily_sales(connection):
    cursor = connection.cursor()
    current_date = datetime.date.today().strftime("%d-%m-%Y")
    select_query = "SELECT r.receipt_id, c.nombre, c.rut, r.payment_method, rd.product_id, p.nombre, rd.quantity, rd.subtotal FROM receipt r INNER JOIN receipt_detail rd ON r.receipt_id = rd.receipt_id INNER JOIN customers c ON r.customer_id = c.customer_id INNER JOIN products p ON rd.product_id = p.product_id WHERE TO_CHAR(r.receipt_date, 'DD-MM-YYYY') = :current_date"
    cursor.execute(select_query, {'current_date': current_date})
    daily_sales = cursor.fetchall()
    return daily_sales