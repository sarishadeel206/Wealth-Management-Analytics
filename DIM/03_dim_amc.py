# Databricks notebook source
amcs = (spark.read.option("header", True).csv("/Volumes/wealth_catalog/raw_zone/amc/amcs.csv"))
amcs.display()

# COMMAND ----------

dim_amc = amcs.select("amc_id","amc_name")
dim_amc.display()

# COMMAND ----------

dim_amc.write.format("delta").mode("overwrite").option("overwriteSchema","true").saveAsTable("wealth_catalog.warehouse.dim_amc")

# COMMAND ----------

spark.table("wealth_catalog.warehouse.dim_amc").display()