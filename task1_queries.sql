
USE ecommerce_sales;

WITH monthly_sales AS (
    SELECT
        DATE_FORMAT(o.order_date, '%Y-%m') AS sales_month,
        SUM(oi.revenue) AS monthly_revenue
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    WHERE o.order_status = 'Delivered'
    GROUP BY DATE_FORMAT(o.order_date, '%Y-%m')
),
revenue_comparison AS (
    SELECT
        sales_month,
        monthly_revenue,
        LAG(monthly_revenue) OVER (
            ORDER BY sales_month
        ) AS previous_month_revenue
    FROM monthly_sales
)
SELECT
    sales_month,
    ROUND(monthly_revenue, 2) AS monthly_revenue,
    ROUND(previous_month_revenue, 2) AS previous_month_revenue,
    ROUND(
        (monthly_revenue - previous_month_revenue)
        / NULLIF(previous_month_revenue, 0) * 100,
        2
    ) AS mom_growth_percentage
FROM revenue_comparison
ORDER BY sales_month;


-- 2. Top 10 Products by Revenue with Category Ranking

WITH product_revenue AS (
    SELECT
        p.product_id,
        p.product_name,
        p.category,
        SUM(oi.revenue) AS total_revenue
    FROM products p
    JOIN order_items oi
        ON p.product_id = oi.product_id
    JOIN orders o
        ON oi.order_id = o.order_id
    WHERE o.order_status = 'Delivered'
    GROUP BY
        p.product_id,
        p.product_name,
        p.category
),
ranked_products AS (
    SELECT
        product_id,
        product_name,
        category,
        total_revenue,
        RANK() OVER (
            PARTITION BY category
            ORDER BY total_revenue DESC
        ) AS category_rank
    FROM product_revenue
)
SELECT
    product_id,
    product_name,
    category,
    ROUND(total_revenue, 2) AS total_revenue,
    category_rank
FROM ranked_products
ORDER BY total_revenue DESC
LIMIT 10;


-- 3. Percentage of Customers with More Than One Order

WITH customer_orders AS (
    SELECT
        customer_id,
        COUNT(DISTINCT order_id) AS total_orders
    FROM orders
    GROUP BY customer_id
)
SELECT
    COUNT(*) AS total_customers,
    SUM(CASE WHEN total_orders > 1 THEN 1 ELSE 0 END)
        AS repeat_customers,
    ROUND(
        SUM(CASE WHEN total_orders > 1 THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*),
        2
    ) AS repeat_customer_percentage
FROM customer_orders;


-- 4. Average Delivery Days by Category and State
-- Identify the 3 slowest states

WITH delivery_analysis AS (
    SELECT
        p.category,
        c.state,
        AVG(o.delivery_days) AS avg_delivery_days
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    JOIN products p
        ON oi.product_id = p.product_id
    JOIN customers c
        ON o.customer_id = c.customer_id
    WHERE o.order_status = 'Delivered'
      AND o.delivery_days IS NOT NULL
    GROUP BY
        p.category,
        c.state
),
state_ranking AS (
    SELECT
        state,
        AVG(avg_delivery_days) AS state_avg_delivery_days,
        RANK() OVER (
            ORDER BY AVG(avg_delivery_days) DESC
        ) AS state_rank
    FROM delivery_analysis
    GROUP BY state
)
SELECT
    d.category,
    d.state,
    ROUND(d.avg_delivery_days, 2) AS avg_delivery_days,
    ROUND(s.state_avg_delivery_days, 2)
        AS state_avg_delivery_days,
    s.state_rank
FROM delivery_analysis d
JOIN state_ranking s
    ON d.state = s.state
WHERE s.state_rank <= 3
ORDER BY
    s.state_rank,
    d.category;


-- 5. Running Total Spending per Customer by Order Date

WITH order_spending AS (
    SELECT
        o.customer_id,
        o.order_id,
        o.order_date,
        SUM(oi.revenue) AS order_revenue
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    WHERE o.order_status = 'Delivered'
    GROUP BY
        o.customer_id,
        o.order_id,
        o.order_date
)
SELECT
    customer_id,
    order_id,
    order_date,
    ROUND(order_revenue, 2) AS order_revenue,
    ROUND(
        SUM(order_revenue) OVER (
            PARTITION BY customer_id
            ORDER BY order_date, order_id
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ),
        2
    ) AS running_total_spending
FROM order_spending
ORDER BY customer_id, order_date, order_id;


-- 6. Top 10% Customers by Lifetime Spending

WITH customer_spending AS (
    SELECT
        o.customer_id,
        SUM(oi.revenue) AS lifetime_spending
    FROM orders o
    JOIN order_items oi
        ON o.order_id = oi.order_id
    WHERE o.order_status = 'Delivered'
    GROUP BY o.customer_id
),
customer_ranking AS (
    SELECT
        customer_id,
        lifetime_spending,
        NTILE(10) OVER (
            ORDER BY lifetime_spending DESC
        ) AS spending_group
    FROM customer_spending
)
SELECT
    customer_id,
    ROUND(lifetime_spending, 2) AS lifetime_spending,
    spending_group
FROM customer_ranking
WHERE spending_group = 1
ORDER BY lifetime_spending DESC;


-- 7. Cancellation and Return Rate by Payment Method

SELECT
    payment_method,
    COUNT(*) AS total_orders,

    SUM(
        CASE
            WHEN order_status = 'Cancelled' THEN 1
            ELSE 0
        END
    ) AS cancelled_orders,

    ROUND(
        SUM(
            CASE
                WHEN order_status = 'Cancelled' THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS cancellation_rate_percentage,

    SUM(
        CASE
            WHEN order_status = 'Returned' THEN 1
            ELSE 0
        END
    ) AS returned_orders,

    ROUND(
        SUM(
            CASE
                WHEN order_status = 'Returned' THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS return_rate_percentage

FROM orders
GROUP BY payment_method
ORDER BY payment_method;

