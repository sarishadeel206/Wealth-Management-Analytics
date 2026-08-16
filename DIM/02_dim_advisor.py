# Databricks notebook source

advisors = (spark.read.option("header", True).csv("/Volumes/wealth_catalog/raw_zone/advisor/advisors.csv"))
advisors.display()

# COMMAND ----------

branches = (spark.read.option("header", True).csv("/Volumes/wealth_catalog/raw_zone/advisor/branches.csv"))
branches.display()

# COMMAND ----------

regions= (spark.read.option("header", True).csv("/Volumes/wealth_catalog/raw_zone/advisor/regions.csv")) 
regions.display()

# COMMAND ----------

dim_advisor=advisors.join(branches,"branch_id","left")
dim_advisor.display()

# COMMAND ----------

dim_branches = branches.join(regions,"region_id","left")
dim_branches.display()

# COMMAND ----------

dim_advisor = dim_advisor.join( regions,"region_id","left")
dim_advisor.display()

# COMMAND ----------

dim_advisor = dim_advisor.select("advisor_id","advisor_name","branch_id", "branch_name", "city","region_id", "region_name", "zone", "joining_date", "status")
dim_advisor.display()

# COMMAND ----------

dim_advisor.write.format("delta").mode("overwrite").option("overwriteSchema","true").saveAsTable("wealth_catalog.warehouse.dim_advisor")

# COMMAND ----------

spark.table("wealth_catalog.warehouse.dim_advisor").display()