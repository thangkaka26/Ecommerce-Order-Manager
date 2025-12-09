USE ecommerce;

-- DISPLAY TOP PRODUCTS REVENUE (KPI)
CREATE VIEW products_revenue_summary AS
SELECT
  products.ProductID, products.ProductName,
  SUM(orderitems.Quantity) AS sold_quantity,
  SUM(orderitems.UnitPrice * orderitems.Quantity) AS revenue
FROM
  products
JOIN orderitems WHERE orderitems.ProductID = products.ProductID
GROUP BY products.productID
ORDER BY revenue DESC;