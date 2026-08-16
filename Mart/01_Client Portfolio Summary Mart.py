# Databricks notebook source
fact_portfolio_aum=spark.table("wealth_catalog.warehouse.fact_portfolio_aum")
fact_portfolio_aum.display()

# COMMAND ----------

dim_client=spark.table("wealth_catalog.warehouse.dim_client")
dim_client.display()

# COMMAND ----------

dim_time = spark.table("wealth_catalog.warehouse.dim_time")
dim_time.display()

# COMMAND ----------

dim_advisor=spark.table("wealth_catalog.warehouse.dim_advisor")
dim_advisor.display()

# COMMAND ----------

fact_portfolio_client=fact_portfolio_aum.join(dim_client.select("client_id","client_name"),"client_id","left")
fact_portfolio_client.display()

# COMMAND ----------

fact_portfolio_advisor=fact_portfolio_client.join(dim_advisor.select("advisor_id","advisor_name"),"advisor_id","left")
fact_portfolio_advisor.display()

# COMMAND ----------

client_portfolio = fact_portfolio_advisor.join(dim_time.select("date_key","full_date"),"date_key","left")
client_portfolio.display()

# COMMAND ----------

from pyspark.sql.functions import(sum,countDistinct,max,col,when)
client_portfolio_summary_mart = client_portfolio.groupBy(
    "client_id",
    "client_name",
    "advisor_name"
).agg(
    sum("cost_value").alias("total_investment"),
    sum("market_value").alias("current_value"),
    sum("gain_loss").alias("gain_loss"),
    countDistinct("scheme_id").alias("active_scheme_count"),
    sum("units_held").alias("total_units"),
    max("full_date").alias("last_updated_date")
)

client_portfolio_summary_mart.display()

# COMMAND ----------

from pyspark.sql.functions import when,col

client_portfolio_summary_mart = client_portfolio_summary_mart.withColumn(
    "gain_percent",
    when(
        col("total_investment") != 0,
        (col("gain_loss") / col("total_investment")) * 100 ).otherwise(0))
client_portfolio_summary_mart.display()

# COMMAND ----------

client_portfolio_summary_mart = client_portfolio_summary_mart.select(
    "client_id",
    "client_name",
    "advisor_name",
    "total_investment",
    "current_value",
    "gain_loss",
    "gain_percent",
    "active_scheme_count",
    "total_units",
    "last_updated_date"
)

client_portfolio_summary_mart.display()

# COMMAND ----------

spark.sql("CREATE SCHEMA IF NOT EXISTS wealth_catalog.mart")

# COMMAND ----------

spark.sql("SHOW SCHEMAS IN wealth_catalog").display()

# COMMAND ----------

client_portfolio_summary_mart.write.format("delta").mode("overwrite").option("overwriteSchema","true").saveAsTable("wealth_catalog.mart.client_portfolio_summary_mart")

# COMMAND ----------

spark.table("wealth_catalog.mart.client_portfolio_summary_mart").display()