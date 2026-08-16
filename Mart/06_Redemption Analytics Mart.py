# Databricks notebook source
fact_redemptions=spark.table("wealth_catalog.warehouse.fact_redemptions")
fact_redemptions.display()

# COMMAND ----------

dim_client=spark.table("wealth_catalog.warehouse.dim_client")
dim_client.display()

# COMMAND ----------

dim_scheme=spark.table("wealth_catalog.warehouse.dim_scheme")
dim_scheme.display()

# COMMAND ----------

dim_time=spark.table("wealth_catalog.warehouse.dim_time")
dim_time.display()

# COMMAND ----------

redemption_client=fact_redemptions.join(dim_client.select("client_id","client_name"),"client_id","left")
redemption_client.display()

# COMMAND ----------

redemption_scheme=redemption_client.join(dim_scheme.select("scheme_id","scheme_name"),"scheme_id","left")
redemption_scheme.display()

# COMMAND ----------

redemption_time=redemption_scheme.join(dim_time.select("date_key","full_date"),"date_key","left")
redemption_time.display()

# COMMAND ----------

from pyspark.sql.functions import month,year,col
redemption_mart=redemption_time.withColumn("redemption_month",month(col("dim_time.full_date"))).withColumn("redemption_year",year(col("dim_time.full_date")))
redemption_mart.display()

# COMMAND ----------

redemption_mart.select(
    "redemption_year"
).distinct().display()

# COMMAND ----------

from pyspark.sql.functions import count, sum, collect_set
redemption_analytics_mart = redemption_mart.groupBy(
    "client_id",
    col("dim_client.client_name"),
    "redemption_month",
    "redemption_year"
).agg(
    collect_set("scheme_name").alias("scheme_name"),
    count("redemption_id").alias("redemption_count"),
    sum("amount").alias("redeemed_amount"),
    sum("units").alias("redeemed_units")
)

redemption_analytics_mart.display()

# COMMAND ----------

redemption_analytics_mart = redemption_analytics_mart.select(
    "client_id",
    "client_name",
    "scheme_name",
    "redemption_count",
    "redeemed_amount",
    "redeemed_units",
    "redemption_month",
    "redemption_year")

redemption_analytics_mart.display()

# COMMAND ----------

redemption_analytics_mart.write.format("delta").mode("overwrite").option("overwriteSchema","true").saveAsTable("wealth_catalog.mart.redemption_analytics_mart")

# COMMAND ----------

spark.table("wealth_catalog.mart.redemption_analytics_mart").display()