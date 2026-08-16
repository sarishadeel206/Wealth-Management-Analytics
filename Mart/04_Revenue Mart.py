# Databricks notebook source
fact_commissions=spark.table("wealth_catalog.warehouse.fact_commissions")
fact_commissions.display()

# COMMAND ----------

dim_advisor=spark.table("wealth_catalog.warehouse.dim_advisor")
dim_advisor.display()

# COMMAND ----------

dim_time=spark.table("wealth_catalog.warehouse.dim_time")
dim_time.display()

# COMMAND ----------

revenue_advisor=fact_commissions.join(dim_advisor.select("advisor_id","advisor_name"),"advisor_id","left")
revenue_advisor.display()

# COMMAND ----------

from pyspark.sql.functions import month,year,col

revenue_time=fact_commissions.withColumn("month",month(col("commission_month"))).withColumn("year",year(col("commission_month")))
revenue_time.display()

# COMMAND ----------

from pyspark.sql.functions import sum,max,col

revenue_mart=revenue_time.groupBy("advisor_id","advisor_name","month","year").agg(sum("brokerage_amount").alias("brokerage_amount"),sum("commission_amount").alias("trail_commission"),(sum(col("brokerage_amount"))+sum(col("commission_amount"))).alias("total_revenue"),max("full_date").alias("last_updated_date"))

revenue_mart.display()

# COMMAND ----------

revenue_mart.write.format("delta").mode("overwrite").option("overwriteSchema","true").saveAsTable("wealth_catalog.mart.revenue_mart")

# COMMAND ----------

spark.table("wealth_catalog.mart.revenue_mart").display()