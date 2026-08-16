# Databricks notebook source
spark.table("wealth_catalog.warehouse.fact_transactions").display()

# COMMAND ----------

spark.table("wealth_catalog.warehouse.fact_sip_installments").display()

# COMMAND ----------

spark.table("wealth_catalog.warehouse.fact_redemptions").display()

# COMMAND ----------

spark.table("wealth_catalog.warehouse.fact_commissions").display()

# COMMAND ----------

spark.table("wealth_catalog.warehouse.fact_portfolio_aum").display()