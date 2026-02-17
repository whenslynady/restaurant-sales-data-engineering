# 🛠️ Project Setup Guide

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/whenslynady/restaurant-sales-data-engineering.git
cd restaurant-sales-data-engineering
````

> Recommended: Use **Ubuntu (WSL)** and open the project with `code .` for better Docker and Python integration.

---

## 2️⃣ Environment Preparation

* Open the project root in **VS Code**
* Install Python and Jupyter extensions when prompted
* Create a `.env` file in the project root:

```
PG_USER=root
PG_PASSWORD=root
PG_HOST=localhost
PG_PORT=5432
PG_DATABASE=restaurant
```
> **Note:** Change `PG_HOST` to `localhost` when running scripts locally without Docker.  
> Keep `pgdatabase` when running from a container connected to the Docker network.


## 3️⃣ Start Docker Containers

Create volume (one-time):

```bash
docker volume create restaurant_postgres_data
docker network create pg-network
```

Run PostgreSQL:

```bash
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="restaurant" \
  -v restaurant_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  --name pgdatabase \
  postgres:18
```

Run pgAdmin (new terminal):

```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8080:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4
```

Access pgAdmin:
`http://localhost:8080`

![Postgres login](images/Postgres_login.png)


# 🔄 Execution Workflow

### Step 1 – Run ETL

* Open **ETL notebook**
* Clean and transform raw data
* Create fact and dimension tables
* Load data into PostgreSQL

![ETL notebook](images/ETL_notebook.png)


````markdown
> **Optional:** You can also use a Python ingestion script instead of the Jupyter Notebook if you prefer automated execution.

## 🐍 Execute Python Script to Ingest Data Locally

```bash
python ingest_data.py --excel_path restaurant_sales_2.xlsx
````

> **Note:** When running locally without Docker, make sure your `.env` has `PG_HOST=localhost`.
> Keep `PG_HOST=pgdatabase` when running from a container connected to the Docker network.

## 🐳 Python Script to Ingest Data into Docker Container

> **Note:** In a real environment, you would not use `--network=pg-network` as a parameter for the container; instead, you would provide the actual URL or IP of your database host.

```bash
# Build the ingestion image
docker build --no-cache -t restaurant-ingestion .

# Run the ingestion container
docker run --rm \
  --network=pg-network \
  -v "$(pwd)":/app \
  restaurant-ingestion:latest \
  --excel_path /app/restaurant_sales_2.xlsx \
  --user root \
  --password root \
  --host pgdatabase \
  --port 5432 \
  --db restaurant
```

### Step 2 – Perform EDA

* Open **EDA notebook**
* Analyze trends, categories, revenue drivers, and performance metrics  

![Perform EDA](images/Perform_EDA.png)

````markdown
> **Note:**  
> - For simple insights, you can use the Jupyter Notebook directly.  
> - For deeper analysis, you can choose to run queries either in the EDA notebook using SQL capabilities or directly inside PostgreSQL.  
> - Jupyter Notebook gives you access to run SQL queries if you prefer, or you can perform analysis inside PostgreSQL itself.  
> - If you want to verify SQL queries directly in PostgreSQL, you can access the SQL console with the following command:  

```bash
docker exec -it <container_name> psql -U root -d restaurant
````

> Example for this project:

```bash
docker exec -it 880d2683d07a psql -U root -d restaurant
```

Once inside the SQL console, here are a few example commands to explore your tables:

```sql
-- List all tables
\dt

-- See the first 5 rows of a table
SELECT * FROM "Fact_Sales" LIMIT 5;

-- Check table structure
\d "Fact_Sales";

-- Count total rows in a table
SELECT COUNT(*) FROM "Fact_Sales";

```

> **Tip:** You can find the SQL exercises and examples in the [SQL_Exercises.md](SetupProject.md) file in the project repository.


### Step 3 – Connect Tableau

* Connect Tableau to PostgreSQL
* Build dashboards
* Refresh and validate KPIs
![Connect Tableau to PostgreSQL](images/Connect_Tableau_PostgreSQL.png)


# 📊 Analytical Dashboards

## 🏷 KPI Executive Banner

The top section of the dashboard displays:
![KPI Banner](images/KPI_Banner.png)

## 📈 Trend Analysis

### Hourly Sales Trend

![Hourly Sales Trend](images/Hourly_Sales_Trend.png)

### Weekly Order Trend

![Weekly Order Trend](images/Weekly_Order_Trend.png)

### Revenue by Category

![Sales by Food Category](images/Sales_Food_Category.png)

### Revenue by Size

![Sales of Food by Size](images/Sales_Food_Size.png)

### Total Orders, Food Sales by Category

![Total Orders and Food Sales by Category](images/Total_Orders_Food_Sales_Category.png)


## 🏆 Top & Bottom Performance

### Top 5 by Revenue

![Top 5 Performing Foods by Revenue](images/Top_5_Performing_Foods_Revenue.png)

### Bottom 5 by Revenue

![Bottom 5 Performing Foods by Revenue](images/Bottom_5_Performing_Foods_Revenue.png)

### Top 5 by Quantity

![Top 5 Food Items by Sales Volume](images/Top_5_Food_Items_Sales_Volume.png)

### Bottom 5 by Quantity

![Bottom 5 Food Items by Sales Volume](images/Bottom_5_Food_Items_Sales_Volume.png)

### Top 5 by Orders

![Top 5 Food by Total Orders](images/Top_5_Foods_Total_Orders.png)

### Bottom 5 by Orders

![Bottom 5 Foods by Total Orders](images/Bottom_5_Foods_Total_Orders.png)



## 🏢 Restaurant Performance

### Quarterly Revenue

![Quarterly Revenue by Restaurant](images/Quarterly_Revenue_Restaurant.png)

### Monthly Distribution

![Revenue Distribution by Restaurant for Each Month](images/Revenue_distribution_restaurant_month.png)

### Orders & Revenue by Day

![Orders and Revenue by Day of Week](images/Orders_Revenue_Day_Week.png)


## 🎯 Promotions & Payment Insights

### Discounted vs Non-Discounted Revenue

![Restaurant Revenue Discounted vs Non-Discounted](images/Restaurant_Revenue_Discounted_vs._Non_Discounted.png)

### Net Revenue by Promotion

![Net Revenue by Discounted Promotion](images/Net_Revenue_Discounted_Promotion.png)

### Revenue & Orders by Payment Method

![Revenue & Orders by Payment Method](images/Revenue_Orders_Payment_Method.png)


## ✅ Final Outcome

This project demonstrates a complete **Data Engineering pipeline**:

Raw Excel Data
→ ETL/EDA Processing
→ PostgreSQL Data Warehouse
→ SQL Analytics
→ Tableau Business Intelligence

The result is a structured, scalable, and reproducible system that transforms raw sales data into actionable business insights.