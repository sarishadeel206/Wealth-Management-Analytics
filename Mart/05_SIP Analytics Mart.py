# Databricks notebook source
fact_sip_installments=spark.table("wealth_catalog.warehouse.fact_sip_installments")
fact_sip_installments.display()

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

sip_client=fact_sip_installments.join(dim_client.select("client_id","client_name"),"client_id","left")
sip_client.display()

# COMMAND ----------

sip_scheme=sip_client.join(dim_scheme.select("scheme_id","scheme_name"),"scheme_id","left")
sip_scheme.display()

# COMMAND ----------

sip_time=sip_scheme.join(dim_time.select("date_key","full_date"),"date_key","left")
sip_time.display()

# COMMAND ----------

from pyspark.sql.functions import sum,count,max,col
sip_analytics_mart=sip_time.groupBy("client_id","client_name","scheme_name").agg(count("sip_id").alias("installment_count"),sum("amount").alias("total_sip_amount"),sum("units").alias("total_units"),max("nav").alias("latest_nav"),sum(col("units")*col("nav")).alias("current_value"))
sip_analytics_mart.display()

# COMMAND ----------

sip_analytics_mart.write.format("delta").mode("overwrite").option("overwriteSchema","true").saveAsTable("wealth_catalog.mart.sip_analytics_mart")

# COMMAND ----------

spark.table("wealth_catalog.mart.sip_analytics_mart").display()