USE ecommerce;

-- REVENUE BY DATE (KPI)
CREATE VIEW revenue_by_date AS
SELECT
  orders.OrderDate,
  COUNT(orders.OrderDate) AS orders_count,
  SUM(orderitems.Quantity * orderitems.UnitPrice) AS revenue
FROM
  orders
JOIN orderitems ON orderitems.OrderID = orders.OrderID
GROUP BY orders.OrderDate
ORDER BY orders.OrderDate DESC;