USE ecommerce;

-- COUNTS OF ORDERS BY STATUS (KPI)
CREATE VIEW orders_by_status AS
SELECT
  orders.Status,
  COUNT(orders.Status) AS total_count
FROM
  orders
GROUP BY orders.Status;