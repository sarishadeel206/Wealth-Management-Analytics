# Databricks notebook source
fact_portfolio_aum = spark.table("wealth_catalog.warehouse.fact_portfolio_aum")
fact_portfolio_aum.display()

# COMMAND ----------

fact_transactions = spark.table("wealth_catalog.warehouse.fact_transactions")
fact_transactions.display()

# COMMAND ----------

fact_commissions = spark.table("wealth_catalog.warehouse.fact_commissions")
fact_commissions.display()

# COMMAND ----------

dim_time = spark.table("wealth_catalog.warehouse.dim_time")
dim_time.display()

# COMMAND ----------

from pyspark.sql.functions import countDistinct,sum,max,col
total_clients = fact_portfolio_aum.agg(countDistinct("client_id").alias("total_clients"))
total_clients.display()

# COMMAND ----------

total_advisors = fact_portfolio_aum.agg(countDistinct("advisor_id").alias("total_advisors"))
total_advisors.display()

# COMMAND ----------

total_aum = fact_portfolio_aum.agg(sum("market_value").alias("total_aum"))
total_aum.display()

# COMMAND ----------

total_investment = fact_transactions.filter(col("transaction_type").isin("PURCHASE","SIP")).agg(sum("amount").alias("total_investment"))
total_investment.display()

# COMMAND ----------

total_redemption = fact_transactions.filter(col("transaction_type")=="REDEMPTION").agg(sum("amount").alias("total_redemption"))
total_redemption.display()

# COMMAND ----------

total_revenue = fact_commissions.agg(sum("commission_amount").alias("total_revenue"))
total_revenue.display()

# COMMAND ----------

active_sips = fact_transactions.filter(col("transaction_type")=="SIP").agg(countDistinct("folio_id").alias("active_sips"))
active_sips.display()

# COMMAND ----------

active_schemes = fact_portfolio_aum.agg(countDistinct("scheme_id").alias("active_schemes"))
active_schemes.display()

# COMMAND ----------

dashboard_date = dim_time.agg(max("full_date").alias("dashboard_date"))
dashboard_date.display()

# COMMAND ----------

executive_dashboard_mart = (
    total_clients
    .crossJoin(total_advisors)
    .crossJoin(total_aum)
    .crossJoin(total_investment)
    .crossJoin(total_redemption)
    .crossJoin(total_revenue)
    .crossJoin(active_sips)
    .crossJoin(active_schemes)
    .crossJoin(dashboard_date))

executive_dashboard_mart.display()

# COMMAND ----------


executive_dashboard_mart.write.format("delta").mode("overwrite").option("overwriteSchema","true").saveAsTable("wealth_catalog.mart.executive_dashboard_mart")

# COMMAND ----------

spark.table("wealth_catalog.mart.executive_dashboard_mart").display()