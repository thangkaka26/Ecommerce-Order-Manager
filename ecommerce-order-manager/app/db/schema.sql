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
  UnitPrice DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (OrderID, ProductID),
  FOREIGN KEY (OrderID) REFERENCES orders(OrderID),
  FOREIGN KEY (ProductID) REFERENCES products(ProductID),
  CONSTRAINT positive_quantity CHECK (Quantity > 0)
);