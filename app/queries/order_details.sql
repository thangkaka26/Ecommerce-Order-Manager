USE ecommerce;

-- DISPLAY ALL ORDER BY CUSTOMERS AND PRODUCTS
CREATE VIEW order_details AS
SELECT
  orders.OrderID,
  customers.CustomerID, customers.CustomerName,
  products.ProductName,
  orders.OrderDate,
  orderitems.Quantity,
  orderitems.Quantity * orderitems.UnitPrice AS total_price,
  orders.Status
FROM
  orders
JOIN orderitems ON orderitems.OrderID = orders.OrderID
JOIN customers ON customers.CustomerID = orders.CustomerID
JOIN products ON products.ProductID = orderitems.ProductID;