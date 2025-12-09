USE ecommerce;

-- DISPLAY ALL CUSTOMERS AND THEIR ORDERS
CREATE VIEW customer_orders AS
SELECT
  customers.CustomerID, customers.CustomerName,
  orders.OrderID, orders.OrderDate, orders.Status
FROM
  customers
LEFT JOIN orders ON orders.CustomerID = customers.CustomerID;