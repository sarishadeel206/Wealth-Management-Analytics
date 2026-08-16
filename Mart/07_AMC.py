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

fact_portfolio_scheme=fact_portfolio_aum.join(dim_scheme.select("scheme_id","amc_id"),"scheme_id","left")
fact_portfolio_scheme.display()

# COMMAND ----------

fact_portfolio_amc=fact_portfolio_scheme.join(dim_amc.select("amc_id","amc_name"),"amc_id","left")
fact_portfolio_amc.display()

# COMMAND ----------

from pyspark.sql.functions import sum,countDistinct,avg,col,when
fact_portfolio_amc=fact_portfolio_amc.withColumn("return_percentage",when(col("cost_value")!=0,(col("gain_loss")/col("cost_value"))*100).otherwise(0))
fact_portfolio_amc.display()

# COMMAND ----------

amc_business_mart=fact_portfolio_amc.groupBy("amc_id","amc_name").agg(sum("market_value").alias("total_aum"),countDistinct("client_id").alias("investor_count"),countDistinct("scheme_id").alias("scheme_count"),avg("return_percentage").alias("average_return"))
amc_business_mart.display()

# COMMAND ----------

amc_business_mart.write.format("delta").mode("overwrite").option("overwriteSchema","true").saveAsTable("wealth_catalog.mart.amc_business_mart")

# COMMAND ----------

fact_portfolio_aum.select("cost_value","market_value","gain_loss").display()

# COMMAND ----------

spark.table("wealth_catalog.mart.amc_business_mart").display()