# Databricks notebook source
from pyspark.sql.functions import *
transactions = spark.read.csv("/Volumes/wealth_catalog/raw_zone/transaction/transactions.csv",header=True,inferSchema=True).display()


# COMMAND ----------

folios = (spark.read.option("header", True).csv("/Volumes/wealth_catalog/raw_zone/transaction/folios.csv"))
folios.display()

# COMMAND ----------

clients = (spark.read.option("header", True).csv("/Volumes/wealth_catalog/raw_zone/client/clients.csv"))
clients.display()

# COMMAND ----------

advisors = ( spark.read.option("header", True).csv("/Volumes/wealth_catalog/raw_zone/advisor/advisors.csv"))
advisors.display()

# COMMAND ----------

schemes = (spark.read.option("header", True).csv("/Volumes/wealth_catalog/raw_zone/scheme/schemes.csv"))
schemes.display()

# COMMAND ----------

transactions_v2 = spark.read.csv(
"/Volumes/wealth_catalog/raw_zone/transaction/transactions_v2.csv",header=True,inferSchema=True)
fact_transactions_folio = transactions_v2.join(folios,"folio_id","left")

fact_transactions_folio.display()

# COMMAND ----------

fact_transactions_client = fact_transactions_folio.join(clients,"client_id","left")
fact_transactions_client.display()

# COMMAND ----------

fact_transactions_advisor = fact_transactions_client.join(advisors,"advisor_id","left")
fact_transactions_advisor.display()

# COMMAND ----------

fact_transactions_scheme  = fact_transactions_advisor.join(schemes,"scheme_id","left")
fact_transactions_scheme .display()

# COMMAND ----------

dim_client = spark.table("wealth_catalog.warehouse.dim_client")
dim_client.display()

# COMMAND ----------

fact_transactions_client = fact_transactions_scheme.join(dim_client.select("client_id"),"client_id","left")
fact_transactions_client.display()

# COMMAND ----------

dim_advisor = spark.table("wealth_catalog.warehouse.dim_advisor")
dim_advisor.display()

# COMMAND ----------

fact_transactions_advisor = fact_transactions_client.join(dim_advisor.select("advisor_id"),"advisor_id","left")
fact_transactions_advisor.display()

# COMMAND ----------

dim_scheme = spark.table("wealth_catalog.warehouse.dim_scheme")
dim_scheme.display()

# COMMAND ----------

fact_transactions_scheme = fact_transactions_advisor.join(dim_scheme.select("scheme_id"),"scheme_id","left")
fact_transactions_scheme.display()

# COMMAND ----------

dim_time = spark.table("wealth_catalog.warehouse.dim_time")
dim_time.display()

# COMMAND ----------

fact_transactions_scheme.select("created_date").show(5, False)

dim_time.select("full_date").show(5, False)

# COMMAND ----------

from pyspark.sql.functions import col, to_date
fact_transactions_date_key = fact_transactions_scheme.join(dim_time.select("full_date", "date_key"),to_date(col("created_date")) == col("full_date"),"left")
fact_transactions_date_key.display()

# COMMAND ----------

transactions_v2 = spark.read.csv(
    "/Volumes/wealth_catalog/raw_zone/transaction/transactions_v2.csv",
    header=True,
    inferSchema=True
)

transactions_v2.display()

# COMMAND ----------

fact_transactions_final = fact_transactions_date_key.select(
    "transaction_id",
    "client_id",
    "advisor_id",
    "scheme_id",
    "date_key",
    "folio_id",
    "transaction_type",
    "amount",
    "units",
    "nav"
)

fact_transactions_final.display()

# COMMAND ----------

fact_transactions_final.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("wealth_catalog.warehouse.fact_transactions")

# COMMAND ----------

spark.table("wealth_catalog.warehouse.fact_transactions").display()