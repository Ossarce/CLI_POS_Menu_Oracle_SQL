import datetime

def get_cashier_username(current_user):
    return current_user[0]['username']

def get_total_sales(cursor):
    current_date = datetime.date.today().strftime("%d-%m-%Y")
    total_sales_query = "SELECT SUM(total_amount) FROM receipt WHERE TO_CHAR(receipt_date, 'DD-MM-YYYY') = :current_date"
    cursor.execute(total_sales_query, {'current_date': current_date})
    total_sales = cursor.fetchone()[0]
    return total_sales

def get_payment_types(cursor):
    current_date = datetime.date.today().strftime("%d-%m-%Y")
    payment_types_query = "SELECT payment_method, COUNT(*) FROM receipt WHERE TO_CHAR(receipt_date, 'DD-MM-YYYY') = :current_date GROUP BY payment_method"
    cursor.execute(payment_types_query, {'current_date': current_date})
    payment_types = {row[0]: row[1] for row in cursor}
    return payment_types

def get_categories(cursor):
    current_date = datetime.date.today().strftime("%d-%m-%Y")
    categories_query = """
        SELECT DISTINCT p.categoria
        FROM products p
        JOIN receipt_detail rd ON p.product_id = rd.product_id
        JOIN receipt r ON rd.receipt_id = r.receipt_id
        WHERE TO_CHAR(r.receipt_date, 'DD-MM-YYYY') = :current_date
    """
    cursor.execute(categories_query, {'current_date': current_date})
    categories = [row[0] for row in cursor]
    return categories