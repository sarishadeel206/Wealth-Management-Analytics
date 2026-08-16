# Databricks notebook source
fact_portfolio_aum=spark.table("wealth_catalog.warehouse.fact_portfolio_aum")
fact_portfolio_aum.display()

# COMMAND ----------

dim_scheme=spark.table("wealth_catalog.warehouse.dim_scheme")
dim_scheme.display()

# COMMAND ----------

dim_amc=spark.table("wealth_catalog.warehouse.dim_amc")
dim_amc.display()

# COMMAND ----------

scheme_portfolio=fact_portfolio_aum.join(dim_scheme.select("scheme_id","scheme_name","category_name","amc_id"),"scheme_id","left")
scheme_portfolio.display()

# COMMAND ----------

scheme_amc=scheme_portfolio.join(dim_amc.select("amc_id","amc_name"),"amc_id","left")
scheme_amc.display()

# COMMAND ----------

from pyspark.sql.functions import sum,countDistinct,max,round,avg
scheme_performance_mart=scheme_amc.groupBy("scheme_id","scheme_name","amc_name","category_name").agg(countDistinct("client_id").alias("investor_count"),sum("market_value").alias("total_aum"),round(avg("gain_loss"),2).alias("average_return"),sum("units_held").alias("units_held"),max("latest_nav").alias("latest_nav"),max("date_key").alias("last_updated_date"))
scheme_performance_mart.display()

# COMMAND ----------

scheme_performance_mart.write.format("delta").mode("overwrite").option("overwriteSchema","true").saveAsTable("wealth_catalog.mart.scheme_performance_mart")

# COMMAND ----------

spark.table("wealth_catalog.mart.scheme_performance_mart").display()