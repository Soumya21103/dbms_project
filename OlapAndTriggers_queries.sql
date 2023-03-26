-- query 1
-- Pivot OLAP Query:
-- Retrieve the total revenue for each product category and month .
 SELECT pc.Cat_ID, 
       SUM(CASE WHEN MONTH(o.O_Date) = 1 THEN o.O_Price ELSE 0 END) AS January_Revenue,
       SUM(CASE WHEN MONTH(o.O_Date) = 2 THEN o.O_Price ELSE 0 END) AS February_Revenue,
       SUM(CASE WHEN MONTH(o.O_Date) = 3 THEN o.O_Price ELSE 0 END) AS March_Revenue,
       SUM(CASE WHEN MONTH(o.O_Date) = 4 THEN o.O_Price ELSE 0 END) AS April_Revenue,
       SUM(CASE WHEN MONTH(o.O_Date) = 5 THEN o.O_Price ELSE 0 END) AS May_Revenue,
       SUM(CASE WHEN MONTH(o.O_Date) = 6 THEN o.O_Price ELSE 0 END) AS June_Revenue,
       SUM(CASE WHEN MONTH(o.O_Date) = 7 THEN o.O_Price ELSE 0 END) AS July_Revenue,
       SUM(CASE WHEN MONTH(o.O_Date) = 8 THEN o.O_Price ELSE 0 END) AS August_Revenue,
       SUM(CASE WHEN MONTH(o.O_Date) = 9 THEN o.O_Price ELSE 0 END) AS September_Revenue,
       SUM(CASE WHEN MONTH(o.O_Date) = 10 THEN o.O_Price ELSE 0 END) AS October_Revenue,
       SUM(CASE WHEN MONTH(o.O_Date) = 11 THEN o.O_Price ELSE 0 END) AS November_Revenue,
       SUM(CASE WHEN MONTH(o.O_Date) = 12 THEN o.O_Price ELSE 0 END) AS December_Revenue
FROM orders o, N_Product p ,prod_cat pc
where o.P_ID = p.NP_id
AND p.Cat_ID = pc.Cat_ID
GROUP BY pc.Cat_ID
order by pc.Cat_ID;
-- query 2
-- Roll-up OLAP Query:
-- Retrieve the total revenue for each quarter
SELECT YEAR(O_Date) AS Year, QUARTER(O_Date) AS Quarter, SUM(O_Price) AS Total_Revenue
FROM orders
GROUP BY YEAR(O_Date), QUARTER(O_Date) with rollup
order by YEAR(O_Date);
-- query 3
-- Drill-down OLAP Query:
-- Retrieve the total revenue for each day of the november for a 3 category.
SELECT o.O_Date, SUM(o.O_Price) AS Total_Revenue
FROM orders o,N_Product p , prod_cat pc
WHERE o.P_ID = p.NP_id
AND p.Cat_ID = pc.Cat_ID
AND YEAR(o.O_Date) = 2022
AND MONTH(o.O_Date) =12
AND pc.Cat_ID = 3
GROUP BY o.O_Date;
-- query 4
-- Total revenue generated by each category and product, including a grand total:

SELECT Cat_Name,pname, SUM(O_price) AS Total_Revenue
FROM Category, N_Product,orders
where Category.Cat_ID = N_Product.Cat_ID
and N_Product.NP_ID = orders.P_ID
GROUP BY Cat_Name,pname WITH ROLLUP;

-- TRIGGERS
-- 1
DELIMITER $$
CREATE TRIGGER remove_items_from_cart
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
  DELETE FROM cart
  WHERE C_ID = NEW.C_ID AND P_ID = NEW.P_ID;
END
$$

-- to check trigger run these

INSERT INTO cart (C_ID, P_ID, Quantity)
VALUES (1, 10, 2), (1, 20, 1);

INSERT INTO orders(O_ID, O_date, O_price, C_ID, P_ID, A_ID,PAY_ID)
VALUES (102, '2023-04-01', 100, 1, 10, 1,101),
       (202, '2023-04-01', 50, 1, 20, 1,101);
-- CHECK IF CART IS EMPTY OR NOT
SELECT * FROM Cart WHERE C_ID = 1;

-- 2
DELIMITER $$
CREATE TRIGGER reduce_product_quantity
AFTER INSERT ON cart
FOR EACH ROW
BEGIN
  UPDATE N_Product
  SET Quantity = Quantity - NEW.Quantity
  WHERE NP_ID = NEW.P_ID;
END $$

-- to check trigger run these
UPDATE N_product
SET Quantity = 1000
WHERE NP_ID = 10;


INSERT INTO Cart (C_ID, P_ID, Quantity)
VALUES (1, 1, 2);


-- Check if quantity has been reduced in normal product table
SELECT * FROM N_Product WHERE NP_id = 1;


 