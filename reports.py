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
    payment_types_query = "SELECT payment_method, COUNT(*) FROM receipt GROUP BY payment_method"
    cursor.execute(payment_types_query)
    payment_types = {row[0]: row[1] for row in cursor}
    return payment_types


def get_categories(cursor):
    categories_query = "SELECT DISTINCT p.categoria FROM products p JOIN receipt_detail rd ON p.product_id = rd.product_id"
    cursor.execute(categories_query)
    categories = {row[0] for row in cursor}
    return categories