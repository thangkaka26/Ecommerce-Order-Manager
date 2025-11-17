CREATE DATABASE ecommerce;

USE ecommerce;

/*
customers
	CustomerID (PK)  |  CustomerName
products
	ProductID (PK)  |  ProductName  |  Price
orders
	OrderID (PK)  |  customerID (FK)  |  orderDate  | Status
orderitems
	OrderID (PK+FK)  |  ProductID (PK+FK)  |  Quantity
*/
CREATE TABLE customers
(
  CustomerID CHAR(8) NOT NULL,
  CustomerName VARCHAR(30) NOT NULL,
  PRIMARY KEY (CustomerID),
  UNIQUE (CustomerID),
  CONSTRAINT customerid_fmt CHECK (CustomerID REGEXP '^C[0-9]{7}$')
);

CREATE TABLE products
(
  ProductID CHAR(8) NOT NULL,
  ProductName VARCHAR(30) NOT NULL,
  Price DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (ProductID),
  UNIQUE (ProductID),
  CONSTRAINT productid_fmt CHECK (ProductID REGEXP '^P[0-9]{7}$'),
  CONSTRAINT positive_price CHECK (Price > 0)
);

CREATE TABLE orders
(
  OrderID CHAR(8) NOT NULL,
  OrderDate DATE NOT NULL,
  Status VARCHAR(10) NOT NULL,
  CustomerID CHAR(8) NOT NULL,
  PRIMARY KEY (OrderID),
  FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID),
  UNIQUE (OrderID),
  CONSTRAINT orderid_fmt CHECK (OrderID REGEXP '^O[0-9]{7}$'),
  CONSTRAINT order_status CHECK (Status IN ('pending', 'processing', 'shipped', 'delivered'))
);

CREATE TABLE orderitems
(
  OrderID CHAR(8) NOT NULL,
  ProductID CHAR(8) NOT NULL,
  Quantity INT NOT NULL,
  PRIMARY KEY (OrderID, ProductID),
  FOREIGN KEY (OrderID) REFERENCES orders(OrderID),
  FOREIGN KEY (ProductID) REFERENCES products(ProductID),
  CONSTRAINT positive_quantity CHECK (Quantity > 0)
);


/*******************/
/*       ADD       */
/*******************/
-- ADD A NEW CUSTOMER
DELIMITER $$
CREATE PROCEDURE add_customer(IN cid CHAR(8), IN cname VARCHAR(30))
BEGIN
  INSERT INTO customers(CustomerID, CustomerName)
  VALUE(cid, cname);
END $$
DEMILIMTER ;

-- ADD A NEW PRODUCT
DELIMITER $$
CREATE PROCEDURE add_product(IN pid CHAR(8), IN pname VARCHAR(30), IN pprice DECIMAL(10,2))
BEGIN
  INSERT INTO products(ProductID, ProductName, Price)
  VALUE(pid, pname, pprice);
END $$
DELIMITER ;

-- ADD AN ORDER (DEFAULT STATUS IS "pending")
DELIMITER $$
CREATE PROCEDURE add_order(IN ordid CHAR(8), IN cid CHAR(8))
BEGIN
  INSERT INTO orders(OrderID, OrderDate, Status, CustomerID)
  VALUE(ordid, CURDATE(), "pending", cid);
END $$
DELIMITER ;

-- ADD AN ORDERITEM (BY ID)
DELIMITER $$
CREATE PROCEDURE add_orderitem(IN ordid CHAR(8), IN pid CHAR(8), IN qty INT)
BEGIN
  INSERT INTO orderitems(OrderID, ProductID, Quantity)
  VALUE(ordid, pid, qty);
END $$
DELIMITER ;


/****************************/
/*         UPDATE          */
/***************************/
-- UPDATE STATUS FOR AN ORDER (BY ID)
DELIMITER $$
CREATE PROCEDURE update_status(IN ordid CHAR(8), IN sts VARCHAR(10))
BEGIN
  UPDATE orders
  SET orders.Status = sts
  WHERE orders.OrderID = ordid;
END $$
DELIMITER ;

-- UPDATE PRICE OF A PRODUCT (BY ID)
DELIMITER $$
CREATE PROCEDURE update_price(IN pid CHAR(8), IN new_prc DECIMAL(10,2))
BEGIN
  UPDATE products
  SET products.Price = new_prc
  WHERE products.ProductID = pid;
END $$
DELIMITER ;


/**********************/
/*       REMOVE       */
/*********************/
-- REMOVE A CUSTOMER (BY ID)
DELIMITER $$
CREATE PROCEDURE delete_customer(IN cid CHAR(8))
BEGIN
  DELETE orderitems FROM orderitems
  JOIN orders ON orders.OrderID = orderitems.OrderID
  WHERE orders.CustomerID = cid;
  DELETE FROM orders WHERE orders.CustomerID = cid;
  DELETE FROM customers WHERE customers.CustomerID = cid;
END $$
DELIMITER ;

-- REMOVE A PRODUCT (BY ID)
DELIMITER $$
CREATE PROCEDURE delete_product(IN pid CHAR(8))
BEGIN
  DELETE FROM orderitems WHERE ProductID = pid;
  DELETE FROM products WHERE ProductID = pid;
END $$
DELIMITER ;

-- REMOVE AN ORDER (BY ID)
DELIMITER $$
CREATE PROCEDURE delete_order(IN ordid CHAR(8))
BEGIN
  DELETE FROM orderitems WHERE orderitems.OrderID = ordid;
  DELETE FROM orders WHERE orders.OrderID = ordid;
END $$
DELIMITER ;

-- REMOVE AN ORDERITEM (BY ID)
DELIMITER $$
CREATE PROCEDURE delete_orderitem(IN ordid CHAR(8), IN pid CHAR(8))
BEGIN
  DELETE FROM orderitems WHERE (OrderID, ProductID) = (ordid, pid);
END $$
DELIMITER ;


/***********************/
/*        SEARCH       */
/***********************/
-- SEARCH CUSTOMERS (BY NAME)
DELIMITER $$
CREATE PROCEDURE search_customer(IN cname VARCHAR(25))
BEGIN
  SELECT * FROM customers
  WHERE CustomerName LIKE CONCAT('%', cname, '%');
END $$
DELIMITER ;

-- SEARCH PRODUCTS (BY NAME)
DELIMITER $$
CREATE PROCEDURE search_product(IN pname VARCHAR(25))
BEGIN
  SELECT * FROM products
  WHERE ProductName LIKE CONCAT('%', pname, '%');
END $$
DELIMITER ;

-- SEARCH AN ORDER WITH ITS DETAILS (BY ID)
DELIMITER $$
CREATE PROCEDURE search_orderdetail(IN ordid CHAR(8))
BEGIN
  SELECT
    orders.OrderID, orders.CustomerID,
    orderitems.ProductID, products.ProductName,
    products.Price AS unit_price,
    orderitems.Quantity, orders.Status
  FROM
    orders
  JOIN orderitems ON orderitems.OrderID = orders.OrderID
  JOIN products ON products.ProductID = orderitems.ProductID
  WHERE orders.OrderID = ordid;
END $$
DELIMITER ;

-- SEARCH A CUSTOMER'S ORDERS (BY ID)
DELIMITER $$
CREATE PROCEDURE search_customer_orders(IN cid CHAR(8))
BEGIN
  SELECT
    customers.CustomerID, customers.CustomerName,
    orders.OrderID, orders.OrderDate, orders.Status
  FROM customers
  JOIN orders ON orders.CustomerID = customers.CustomerID
  WHERE customers.CustomerID = cid;
END $$
DELIMITER ;


/**************************/
/*         VIEWS          */
/**************************/
-- DISPLAY ALL ORDER BY CUSTOMERS AND PRODUCTS
CREATE VIEW order_details AS
SELECT
  orders.OrderID,
  customers.CustomerID, customers.CustomerName,
  products.ProductName,
  orders.OrderDate,
  orderitems.Quantity,
  orderitems.Quantity * products.Price AS total_price,
  orders.Status
FROM
  orders
JOIN orderitems ON orderitems.OrderID = orders.OrderID
JOIN customers ON customers.CustomerID = orders.CustomerID
JOIN products ON products.ProductID = orderitems.ProductID;

-- DISPLAY ALL CUSTOMERS AND THEIR ORDERS
CREATE VIEW customer_orders AS
SELECT
  customers.CustomerID, customers.CustomerName,
  orders.OrderID, orders.OrderDate, orders.Status
FROM
  customers
LEFT JOIN orders ON orders.CustomerID = customers.CustomerID;

-- DISPLAY ORDER SUMMARY (KPI)
CREATE VIEW products_revenue_summary AS
SELECT
  products.ProductID, products.ProductName,
  SUM(orderitems.Quantity) AS sold_quantity,
  SUM(products.Price * orderitems.Quantity) AS revenue
FROM
  products
JOIN orderitems WHERE orderitems.ProductID = products.ProductID
GROUP BY products.productID
ORDER BY revenue DESC;

-- COUNTS OF ORDERS BY STATUS (KPI)
CREATE VIEW orders_by_status AS
SELECT
  orders.Status,
  COUNT(orders.Status) AS total_count
FROM
  orders
GROUP BY orders.Status;

-- REVENUE TO DATE (KPI)
CREATE VIEW revenue_to_date AS
SELECT
  orders.OrderDate,
  COUNT(orders.OrderDate) AS orders_count,
  SUM(orderitems.Quantity * products.Price) AS revenue
FROM
  orders
JOIN orderitems ON orderitems.OrderID = orders.OrderID
JOIN products ON products.ProductID = orderitems.ProductID
GROUP BY orders.OrderDate
ORDER BY orders.OrderDate DESC;