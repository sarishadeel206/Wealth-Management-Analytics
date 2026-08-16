# Databricks notebook source
clients = (spark.read.option("header", True).csv("/Volumes/wealth_catalog/raw_zone/client/clients.csv"))
clients.display()

# COMMAND ----------

risk_profiles = (spark.read.option("header", True).csv("/Volumes/wealth_catalog/raw_zone/client/risk_profiles.csv"))
risk_profiles.display()

# COMMAND ----------

dim_client = clients.join(risk_profiles,"client_id", "left")

dim_client.display()

# COMMAND ----------


dim_client = dim_client.select("client_id","client_name","dob","pan","mobile","email","city","state", "advisor_id","risk_category", "risk_score","onboarding_date")
dim_client.display()

# COMMAND ----------


dim_client = dim_client.select("client_id","client_name","dob","pan","mobile", "email","city", "state", "advisor_id","risk_category", "risk_score", "onboarding_date")

dim_client.display()

# COMMAND ----------

dim_client.write.format("delta").mode("overwrite").option("overwriteSchema","true").saveAsTable("wealth_catalog.warehouse.dim_client")

# COMMAND ----------

spark.table("wealth_catalog.warehouse.dim_client").display() #verify