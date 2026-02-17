# SQL Exercises for Restaurant Sales Analysis

## 1️⃣ Total Revenue (including discounts)
```sql
SELECT ROUND(SUM(total_amount_discounted)::numeric, 2) AS total_revenue
FROM "Fact_Sales";
````

## 2️⃣ Total Profit Generated

```sql
SELECT ROUND(SUM((unit_price - food_cost) * quantity)::numeric, 2) AS total_profit
FROM "Fact_Sales";
```

## 3️⃣ Total Number of Orders

```sql
SELECT COUNT(DISTINCT sale_id) AS total_orders
FROM "Fact_Sales";
```

## 4️⃣ Total Number of Food Items Sold

```sql
SELECT SUM(quantity) AS total_food_sold
FROM "Fact_Sales";
```

## 5️⃣ Average Number of Food Items per Order

```sql
SELECT ROUND((SUM(quantity)::decimal / COUNT(DISTINCT sale_id))::numeric, 2) AS average_food_per_order
FROM "Fact_Sales";
```

## 6️⃣ Average Revenue per Order

```sql
SELECT ROUND((SUM(total_amount_discounted)::decimal / COUNT(DISTINCT sale_id))::numeric, 2) AS average_revenue_per_order
FROM "Fact_Sales";
```

## 7️⃣ Combined KPI Query

```sql
SELECT 
    ROUND(SUM(total_amount_discounted)::numeric, 2) AS total_revenue,
    ROUND(SUM((unit_price - food_cost) * quantity)::numeric, 2) AS total_profit,
    COUNT(DISTINCT sale_id) AS total_orders,
    SUM(quantity) AS total_food_sold,
    ROUND((SUM(quantity)::decimal / COUNT(DISTINCT sale_id))::numeric, 2) AS average_food_per_order,
    ROUND((SUM(total_amount_discounted)::decimal / COUNT(DISTINCT sale_id))::numeric, 2) AS average_revenue_per_order
FROM "Fact_Sales";
```

## 8️⃣ Order Distribution by Hour and Food Category

```sql
SELECT 
    EXTRACT(HOUR FROM order_datetime) AS "Hour of the Day",
    SUM(quantity) AS "Total Food Sold"
FROM "Fact_Sales"
GROUP BY EXTRACT(HOUR FROM order_datetime)
ORDER BY "Hour of the Day";
```

## 9️⃣ Weekly Trend of Total Orders

```sql
WITH weekly_orders AS (
    SELECT
        DATE_TRUNC('week', order_datetime)::date AS week_start,
        COUNT(DISTINCT sale_id) AS total_orders,
        DATE_PART('week', order_datetime) AS week_num
    FROM "Fact_Sales"
    WHERE order_datetime IS NOT NULL
    GROUP BY week_start, week_num
),
filtered AS (
    SELECT *
    FROM weekly_orders
    WHERE week_num <= 52
    ORDER BY week_start
    OFFSET 1
)
SELECT *
FROM filtered
ORDER BY week_start;
```

## 🔟 Order Frequency by Month

```sql
SELECT 
    TRIM(TO_CHAR(order_datetime, 'Month')) AS "Month",
    COUNT(DISTINCT sale_id) AS "Frequency"
FROM "Fact_Sales"
WHERE order_datetime IS NOT NULL
GROUP BY EXTRACT(MONTH FROM order_datetime),
         TRIM(TO_CHAR(order_datetime, 'Month'))
ORDER BY EXTRACT(MONTH FROM order_datetime);
```

## 1️⃣1️⃣ Revenue Distribution by Food Size

```sql
WITH revenue_by_size AS (
    SELECT 
        di.item_size,
        SUM(fs.total_amount_discounted)::numeric AS revenue_with_discount
    FROM "Fact_Sales" fs
    JOIN "Dim_Items" di 
        ON fs.item_id = di.item_id
    WHERE di.item_size IS NOT NULL
      AND fs.total_amount_discounted IS NOT NULL
    GROUP BY di.item_size
)
SELECT
    item_size AS "Food Size",
    ROUND(revenue_with_discount, 2) AS "Revenue with Discount",
    ROUND(
        (revenue_with_discount / SUM(revenue_with_discount) OVER ()) * 100,
        2
    ) AS "Percentage of Total"
FROM revenue_by_size
ORDER BY revenue_with_discount DESC;
```

## 1️⃣2️⃣ Revenue Distribution by Food Category

```sql
SELECT
    di.category AS "Food Category",
    COUNT(DISTINCT fs.sale_id) AS "Total Orders",
    SUM(fs.quantity) AS "Total Food Sold"
FROM "Fact_Sales" fs
JOIN "Dim_Items" di
    ON fs.item_id = di.item_id
WHERE di.category IS NOT NULL
GROUP BY di.category
ORDER BY "Total Orders" ASC;
```

## 1️⃣3️⃣ Top 5 Foods by Total Revenue

```sql
SELECT
    di.item_name AS "Food Name",
    ROUND(SUM(fs.total_amount_discounted)::numeric, 2) AS "Total Revenue"
FROM "Fact_Sales" fs
JOIN "Dim_Items" di
    ON fs.item_id = di.item_id
GROUP BY di.item_name
ORDER BY SUM(fs.total_amount_discounted) DESC
LIMIT 5;
```


### 1️⃣4️⃣ Bottom 5 Foods by Total Revenue

```sql
SELECT
    di.item_name AS "Food Name",
    ROUND(SUM(fs.total_amount_discounted)::numeric, 2) AS "Total Revenue"
FROM "Fact_Sales" fs
JOIN "Dim_Items" di
    ON fs.item_id = di.item_id
GROUP BY di.item_name
ORDER BY SUM(fs.total_amount_discounted) ASC
LIMIT 5;
```

---

### 1️⃣5️⃣ Top 5 Foods by Quantity Sold

```sql
SELECT
    di.item_name AS "Food Name",
    SUM(fs.quantity) AS "Total Quantity Sold"
FROM "Fact_Sales" fs
JOIN "Dim_Items" di
    ON fs.item_id = di.item_id
GROUP BY di.item_name
ORDER BY SUM(fs.quantity) DESC
LIMIT 5;
```

---

### 1️⃣6️⃣ Bottom 5 Foods by Quantity Sold

```sql
SELECT
    di.item_name AS "Food Name",
    SUM(fs.quantity) AS "Total Quantity Sold"
FROM "Fact_Sales" fs
JOIN "Dim_Items" di
    ON fs.item_id = di.item_id
GROUP BY di.item_name
ORDER BY SUM(fs.quantity) ASC
LIMIT 5;
```

---

### 1️⃣7️⃣ Top 5 Foods by Total Orders

```sql
SELECT
    di.item_name AS "Food Name",
    COUNT(DISTINCT fs.order_id) AS "Total Orders"
FROM "Fact_Sales" fs
JOIN "Dim_Items" di
    ON fs.item_id = di.item_id
GROUP BY di.item_name
ORDER BY COUNT(DISTINCT fs.order_id) DESC
LIMIT 5;
```

---

### 1️⃣8️⃣ Bottom 5 Foods by Total Orders

```sql
SELECT
    di.item_name AS "Food Name",
    COUNT(DISTINCT fs.sale_id) AS "Number of Orders"
FROM "Fact_Sales" fs
JOIN "Dim_Items" di
    ON fs.item_id = di.item_id
GROUP BY di.item_name
ORDER BY COUNT(DISTINCT fs.sale_id) ASC
LIMIT 5;
```

---

### 1️⃣9️⃣ Quarterly Revenue by Restaurant

```sql
SELECT
    r.restaurant_name AS "Restaurant Name",
    TO_CHAR(fs.order_datetime, 'YYYY-"Q"Q') AS "Quarter",
    ROUND(SUM(fs.total_amount_discounted)::numeric, 2) AS "Total Revenue"
FROM "Fact_Sales" fs
JOIN "Dim_Restaurants" r
    ON fs.restaurant_id = r.restaurant_id
GROUP BY r.restaurant_name, TO_CHAR(fs.order_datetime, 'YYYY-"Q"Q')
ORDER BY r.restaurant_name, "Quarter";
```

---

### 2️⃣0️⃣ Revenue Distribution With and Without Discounts by Restaurant

```sql
WITH revenue_flagged AS (
    SELECT
        r.restaurant_name AS "Restaurant Name",
        CASE 
            WHEN fs.total_amount_discounted < fs.total_amount THEN fs.total_amount_discounted
            ELSE 0
        END AS revenue_with_discount,
        CASE 
            WHEN fs.total_amount_discounted >= fs.total_amount THEN fs.total_amount
            ELSE 0
        END AS revenue_without_discount
    FROM "Fact_Sales" fs
    JOIN "Dim_Restaurants" r
        ON fs.restaurant_id = r.restaurant_id
)

SELECT
    "Restaurant Name",
    ROUND(SUM(revenue_with_discount)::numeric, 2) AS revenue_with_discount,
    ROUND(SUM(revenue_without_discount)::numeric, 2) AS revenue_without_discount
FROM revenue_flagged
GROUP BY "Restaurant Name"
ORDER BY "Restaurant Name";
```

---

### 2️⃣1️⃣ Monthly Revenue Distribution by Restaurant

```sql
WITH monthly_revenue AS (
    SELECT
        r.restaurant_name AS restaurant_name,
        TO_CHAR(fs.order_datetime, 'YYYY-MM') AS month,
        SUM(fs.total_amount_discounted)::numeric AS total_revenue
    FROM "Fact_Sales" fs
    JOIN "Dim_Restaurants" r
        ON fs.restaurant_id = r.restaurant_id
    GROUP BY r.restaurant_name, TO_CHAR(fs.order_datetime, 'YYYY-MM')
)

SELECT
    restaurant_name,
    month,
    ROUND(total_revenue, 2) AS total_revenue
FROM monthly_revenue
ORDER BY restaurant_name, month;
```

---

### 2️⃣2️⃣ Distribution of Orders and Total Revenue by Day of the Week

```sql
WITH weekly_distribution AS (
    SELECT
        TO_CHAR(order_datetime, 'Day') AS day_of_week,
        COUNT(DISTINCT sale_id) AS number_of_orders,
        SUM(total_amount_discounted)::numeric AS total_revenue
    FROM "Fact_Sales"
    GROUP BY TO_CHAR(order_datetime, 'Day')
)

SELECT
    day_of_week,
    number_of_orders,
    ROUND(total_revenue, 2) AS total_revenue
FROM weekly_distribution
ORDER BY
    CASE TRIM(day_of_week)
        WHEN 'Monday' THEN 1
        WHEN 'Tuesday' THEN 2
        WHEN 'Wednesday' THEN 3
        WHEN 'Thursday' THEN 4
        WHEN 'Friday' THEN 5
        WHEN 'Saturday' THEN 6
        WHEN 'Sunday' THEN 7
    END;
```

---

### 2️⃣3️⃣ Net Revenue by Discounted Promotion

```sql
WITH promotion_revenue AS (
    SELECT
        dp."discount_name",
        SUM(fs."total_amount_discounted")::numeric AS total_revenue
    FROM "Fact_Sales" fs
    LEFT JOIN "Dim_Promotions" dp
        ON fs."promo_id" = dp."promo_id"
    WHERE dp."discount_name" IS NOT NULL
    GROUP BY dp."discount_name"
)

SELECT
    "discount_name",
    ROUND(total_revenue, 2) AS total_revenue
FROM promotion_revenue
ORDER BY total_revenue DESC;
```

---

### 2️⃣4️⃣ Total Revenue and Number of Orders by Payment Method

```sql
WITH payment_summary AS (
    SELECT
        dp."payment_method",
        SUM(fs."total_amount_discounted")::numeric AS total_revenue,
        COUNT(DISTINCT fs."sale_id") AS number_of_orders
    FROM "Fact_Sales" fs
    LEFT JOIN "Dim_Payments" dp
        ON fs."payment_id" = dp."payment_id"
    GROUP BY dp."payment_method"
)

SELECT
    "payment_method",
    ROUND(total_revenue, 2) AS total_revenue,
    number_of_orders
FROM payment_summary
ORDER BY total_revenue DESC;
```

---

### 2️⃣5️⃣ Staff Member with the Highest Food Sales

```sql
WITH staff_sales AS (
    SELECT
        ds."staff_name",
        ROUND(SUM(fs."total_amount_discounted")::numeric, 2) AS total_sales
    FROM "Fact_Sales" fs
    LEFT JOIN "Dim_Staff" ds
        ON fs."staff_id" = ds."staff_id"
    GROUP BY ds."staff_name"
)
SELECT *
FROM staff_sales
ORDER BY total_sales DESC
LIMIT 5;
```
