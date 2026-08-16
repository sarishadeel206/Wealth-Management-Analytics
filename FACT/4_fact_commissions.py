# Databricks notebook source
brokerage = spark.read.csv("/Volumes/wealth_catalog/raw_zone/revenue/brokerage.csv", header=True, inferSchema=True)
brokerage.display()

# COMMAND ----------

trail_commissions = spark.read.csv("/Volumes/wealth_catalog/raw_zone/revenue/trail_commissions.csv", header=True, inferSchema=True)
trail_commissions.display()

# COMMAND ----------

advisors = spark.read.csv("/Volumes/wealth_catalog/raw_zone/advisor/advisors.csv", header=True, inferSchema=True)
advisors.display()

# COMMAND ----------

schemes = spark.read.csv("/Volumes/wealth_catalog/raw_zone/scheme/schemes.csv", header=True, inferSchema=True)
schemes.display()

# COMMAND ----------

fact_commissions_trail = brokerage.join(trail_commissions, "advisor_id", "left")
fact_commissions_trail.display()

# COMMAND ----------

fact_commissions_advisor = fact_commissions_trail.join(advisors, "advisor_id", "left")
fact_commissions_advisor.display()

# COMMAND ----------

fact_commissions_scheme = fact_commissions_advisor.join(schemes, "scheme_id", "left")
fact_commissions_scheme.display()

# COMMAND ----------

dim_time = spark.table("wealth_catalog.warehouse.dim_time")
dim_time.display()

# COMMAND ----------

from pyspark.sql.functions import col, to_date
fact_commissions_date_key = fact_commissions_scheme.join(dim_time.select("full_date","date_key"),to_date(col("commission_month")) == col("full_date"),"left")
fact_commissions_date_key.display()

# COMMAND ----------

fact_commissions_date_key.write.format("delta").mode("overwrite").option("overwriteSchema","true").saveAsTable("wealth_catalog.warehouse.fact_commissions")

# COMMAND ----------

spark.table("wealth_catalog.warehouse.fact_redemptions").display()