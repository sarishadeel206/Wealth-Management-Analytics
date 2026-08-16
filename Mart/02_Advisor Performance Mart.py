# Databricks notebook source
fact_portfolio_aum = spark.table("wealth_catalog.warehouse.fact_portfolio_aum")
fact_portfolio_aum.display()

# COMMAND ----------

fact_commissions = spark.table("wealth_catalog.warehouse.fact_commissions")
fact_commissions.display()

# COMMAND ----------

dim_advisor = spark.table("wealth_catalog.warehouse.dim_advisor")
dim_advisor.display()

# COMMAND ----------

dim_client = spark.table("wealth_catalog.warehouse.dim_client")
dim_client.display()

# COMMAND ----------

dim_time = spark.table("wealth_catalog.warehouse.dim_time")
dim_time.display()

# COMMAND ----------

advisor_portfolio = fact_portfolio_aum.join(
    dim_advisor.select("advisor_id","advisor_name"),
    on="advisor_id",
    how="left")
advisor_portfolio.display()

# COMMAND ----------

advisor_client = advisor_portfolio.join(
    dim_client.select("client_id","client_name"),
    on="client_id",
    how="left")
advisor_client.display()

# COMMAND ----------

fact_commission_selected = fact_commissions.select(
    "advisor_id",
    "scheme_id",
    "commission_amount",
    "brokerage_amount",
    "date_key")
fact_commission_selected.display()

# COMMAND ----------

advisor_commission = advisor_client.join(
    fact_commission_selected,
    ["advisor_id","scheme_id"],
    "left")
advisor_commission.display()

# COMMAND ----------

dim_time_selected = dim_time.select(
    "date_key",
    "full_date")
dim_time_selected.display()

# COMMAND ----------

advisor_performance = advisor_commission.join(
    dim_time_selected,
    "date_key",
    "left")
advisor_performance.display()

# COMMAND ----------

from pyspark.sql.functions import *
advisor_performance_mart = advisor_performance.groupBy(
    "advisor_id",
    "advisor_name"
).agg(
    countDistinct("client_id").alias("total_clients"),
    sum("market_value").alias("total_aum"),
    sum("commission_amount").alias("total_commission"),
    sum("brokerage_amount").alias("total_revenue"),
    avg("market_value").alias("average_client_aum"),
    max("full_date").alias("last_updated_date"))
advisor_performance_mart.display()

# COMMAND ----------

fact_commission_selected.count()

# COMMAND ----------

fact_commission_selected.select(
    "advisor_id",
    "scheme_id",
    "commission_amount",
    "brokerage_amount"
).display()

# COMMAND ----------

advisor_commission.select(
    "advisor_id",
    "scheme_id",
    "commission_amount",
    "brokerage_amount"
).display()

# COMMAND ----------

fact_portfolio_aum.select(
    "advisor_id",
    "scheme_id"
).display()

# COMMAND ----------

fact_commissions.select(
    "advisor_id",
    "scheme_id"
).display()

# COMMAND ----------

advisor_performance_mart.write.format("delta").mode("overwrite").option("overwriteSchema","true").saveAsTable("wealth_catalog.mart.advisor_performance_mart")

# COMMAND ----------

spark.table("wealth_catalog.mart.advisor_performance_mart").display()