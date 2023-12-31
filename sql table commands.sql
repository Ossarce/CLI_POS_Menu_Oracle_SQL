CREATE TABLE products (
  product_id NUMBER PRIMARY KEY,
  codigo NUMBER,
  nombre VARCHAR2(100),
  categoria VARCHAR2(100),
  stock NUMBER,
  precio NUMBER
);

CREATE TABLE users (
  user_id NUMBER PRIMARY KEY,
  username VARCHAR2(100),
  password VARCHAR2(100)
);

CREATE TABLE customers (
  customer_id NUMBER PRIMARY KEY,
  nombre VARCHAR2(100),
  apellido VARCHAR2(100),
  rut NUMBER,
  email VARCHAR2(100),
  telefono NUMBER
);


CREATE TABLE receipt (
  receipt_id NUMBER PRIMARY KEY,
  customer_id NUMBER,
  cashier_id NUMBER,
  total_amount NUMBER(10, 2),
  payment_method VARCHAR2(50),
  receipt_date DATE,
  CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
  CONSTRAINT fk_cashier FOREIGN KEY (cashier_id) REFERENCES users(user_id)
);


CREATE TABLE receipt_detail (
  detail_id NUMBER PRIMARY KEY,
  receipt_id NUMBER,
  product_id NUMBER,
  quantity NUMBER,
  price NUMBER(10, 2),
  subtotal NUMBER(10, 2),
  CONSTRAINT fk_receipt FOREIGN KEY (receipt_id) REFERENCES receipt(receipt_id),
  CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Estos son los sequences y triggers (Crean las ids de forma automatica)
-- Products
CREATE SEQUENCE product_id_seq START WITH 1 INCREMENT BY 1;


CREATE OR REPLACE TRIGGER product_id_trigger
BEFORE INSERT ON products
FOR EACH ROW
BEGIN
  :NEW.product_id := product_id_seq.NEXTVAL;
END;
/

-- Users
CREATE SEQUENCE user_id_seq START WITH 1 INCREMENT BY 1;


CREATE OR REPLACE TRIGGER user_id_trigger
BEFORE INSERT ON users
FOR EACH ROW
BEGIN
  :NEW.user_id := user_id_seq.NEXTVAL;
END;
/

-- Customers
CREATE SEQUENCE customer_id_seq START WITH 1 INCREMENT BY 1;


CREATE OR REPLACE TRIGGER customer_id_trigger
BEFORE INSERT ON customers
FOR EACH ROW
BEGIN
  :NEW.customer_id := customer_id_seq.NEXTVAL;
END;
/

-- Receipts
CREATE SEQUENCE receipt_id_seq START WITH 1 INCREMENT BY 1;


CREATE OR REPLACE TRIGGER receipt_id_trigger
BEFORE INSERT ON receipt
FOR EACH ROW
BEGIN
  :NEW.receipt_id := receipt_id_seq.NEXTVAL;
END;
/

-- Receipt Detail
CREATE SEQUENCE detail_id_seq START WITH 1 INCREMENT BY 1;


CREATE OR REPLACE TRIGGER detail_id_trigger
BEFORE INSERT ON receipt_detail
FOR EACH ROW
BEGIN
  :NEW.detail_id := detail_id_seq.NEXTVAL;
END;
/
