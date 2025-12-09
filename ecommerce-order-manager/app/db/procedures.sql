USE ecommerce;


/********** ADD **********/
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
  DECLARE prc DECIMAL(10,2);
  SELECT Price INTO prc FROM products WHERE ProductID = pid;
  INSERT INTO orderitems(OrderID, ProductID, Quantity, UnitPrice)
  VALUE(ordid, pid, qty, prc);
END $$
DELIMITER ;


/********** DELETE **********/
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


/********** SEARCH **********/
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
    orderitems.UnitPrice,
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


/********** UPDATE **********/
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