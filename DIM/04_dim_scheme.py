# Databricks notebook source
schemes = (spark.read.option("header", True).csv("/Volumes/wealth_catalog/raw_zone/scheme/schemes.csv"))
schemes.display()

# COMMAND ----------

scheme_categories = (spark.read.option("header", True).csv("/Volumes/wealth_catalog/raw_zone/scheme/scheme_categories.csv"))
scheme_categories.display()

# COMMAND ----------

amcs = (spark.read.option("header", True).csv("/Volumes/wealth_catalog/raw_zone/amc/amcs.csv"))
amcs.display()

# COMMAND ----------

dim_scheme = schemes.join(scheme_categories,"category_id", "left")
dim_scheme.display()

# COMMAND ----------

dim_scheme = dim_scheme.join(amcs, "amc_id","left")
dim_scheme.display()

# COMMAND ----------

dim_scheme = dim_scheme.select("scheme_id","scheme_name","amc_id","amc_name","category_id","category_name", "asset_class","risk_level", "expense_ratio")
dim_scheme.display()

# COMMAND ----------

dim_scheme.write.format("delta").mode("overwrite").option("overwriteSchema","true").saveAsTable("wealth_catalog.warehouse.dim_scheme")

# COMMAND ----------

spark.table("wealth_catalog.warehouse.dim_scheme").display()