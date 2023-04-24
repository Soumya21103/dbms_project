-- QUERY-1:
-- Returns the order ID, shipment ID, mode of transport and product name of all orders that have a status of "Delivering" in the shipment table

SELECT o.O_ID, s.Shipment_ID, s.mode_of_Trans, n.PName
FROM ORDERS o, Shipment s,n_product n
where o.O_ID = s.O_ID and o.p_ID = n.np_ID and s.status = 'Delivering';


-- QUERY-2:
-- Returns the total amount to pay in the cart by the customer on products in each category

SELECT c.First_Name, c.Last_name, cat.Cat_Name, SUM(cp.Price * ca.Quantity) AS total_spent
FROM Customer c, cart ca,n_product cp, Category cat
where  c.C_ID = ca.C_ID
and ca.P_ID = cp.nP_ID and cp.Cat_ID = cat.Cat_ID
GROUP BY c.C_ID, cat.Cat_ID;

-- QUERY-3:
-- Updates the password of a specific customer

UPDATE Customer
SET Password = 'DBMSRICHFLEX'
WHERE C_ID = 9;
 
-- Query-4:
-- Deletes the review with review id 26

DELETE FROM Review
where Rw_ID=26;
 
-- Query-5:

-- Create a view that shows the total number of orders by the customer.
-- And using that to get the number of orders for a particular customer

CREATE VIEW OrdersBy_Customers AS
SELECT C_ID, COUNT(*) AS NumOrders
FROM ORDERS
GROUP BY C_ID;

SELECT c.First_name, c.Last_name, o.NumOrders
FROM Customer c, OrdersBy_Customers o 
where c.C_ID = o.C_ID;

-- Query-6:
-- Returns the names of customers who have placed more than two orders and the count of their orders.

SELECT DISTINCT c.First_Name, COUNT(o.O_ID) AS num_orders
FROM Customer c, Orders o 
where c.C_ID = o.C_ID
GROUP BY c.C_ID
HAVING COUNT(o.O_ID) > 2;

-- Query-7:

-- using the natural join operation to combine tables based on their common attributes. 
-- and returning the first name, last name, order ID, order price, and product name for all customers who are 18 or older and have ordered a product that costs more than 100000 Rs.

SELECT c.First_name, c.Last_name, o.O_ID, o.O_price, p.PName
FROM Customer c
NATURAL JOIN ORDERS o
NATURAL JOIN n_product p
WHERE c.Age >= 18 AND p.Price > 100000;

-- Query-8:
-- Using difference operations to find the customers who have not made any orders

SELECT c.C_ID, c.First_name, c.Last_name FROM Customer c
WHERE NOT EXISTS (
  SELECT * FROM ORDERS o WHERE c.C_ID = o.C_ID
);


-- Query-9:
-- returns the first name, last name, order ID, order date, and shipment status for all orders cancelled in the year 2022.


SELECT c.First_name, c.Last_name, o.O_ID, o.O_date, s.status
FROM Customer c
INNER JOIN ORDERs o ON c.C_ID = o.C_ID
INNER JOIN Shipment s ON o.O_ID = s.O_ID
WHERE s.status = 'Cancelled' AND YEAR(o.O_date) = 2022;

-- Query 10
-- Returns the Retailer name, Order date and price, Product name and price for all orders of products 
-- in category one placed by retailers whose sales are greater than 100000 
-- and then printing the results ordered by order price in descending order.

SELECT R.Name AS RetailerName, O.O_date AS OrderDate, O.O_price AS OrderPrice, P.PName AS ProductName, P.Price AS ProductPrice 
FROM Retailer R 
LEFT JOIN Orders O ON R.R_ID = O.A_ID 
LEFT JOIN n_Product P ON O.P_ID = P.nP_ID 
WHERE R.R_Sale > 50 AND P.Cat_ID = 1 
ORDER BY O.O_price DESC;

-- Query 11
-- calculates the total sales for each retailer by summing the order price of their products.
-- And groups the result by the retailer's name

SELECT R.Name, SUM(O.O_price) AS Total_sales
FROM Retailer R,n_product P , ORDERS O 
WHERE R.R_ID = P.R_ID
AND P.nP_ID = O.P_ID
GROUP BY R.Name;

-- Query 12
-- Returns payment information along with customer name 
-- and sorts the result by payment id in ascending order.

SELECT P.payment_id, P.c_id, P.o_id, C.First_name, C.Last_name,P.medium, P.amount
FROM payment P, Customer C 
WHERE P.c_id = C.C_ID
ORDER BY P.payment_id;

-- Query 13
--  returns the total amount to pay in the cart by the customer on products
SELECT c.C_ID, SUM(cp.Price * ca.Quantity) AS total_amount
FROM Customer c, cart ca, n_product cp
WHERE c.C_ID = ca.C_ID AND ca.P_ID = cp.nP_ID
GROUP BY c.C_ID;
