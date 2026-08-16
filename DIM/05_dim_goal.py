# Databricks notebook source

goals = (spark.read.option("header", True).csv("/Volumes/wealth_catalog/raw_zone/goal/goals.csv"))
goals.display()

# COMMAND ----------

dim_goal = goals.select("goal_id","goal_name", "target_amount","target_date")
dim_goal.display()

# COMMAND ----------

dim_goal.write.format("delta").mode("overwrite").option("overwriteSchema","true").saveAsTable("wealth_catalog.warehouse.dim_goal")

# COMMAND ----------

spark.table("wealth_catalog.warehouse.dim_goal").display() #verify