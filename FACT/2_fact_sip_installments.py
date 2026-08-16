# Databricks notebook source
sip_installments = spark.read.csv("/Volumes/wealth_catalog/raw_zone/transaction/sip_installments.csv",header=True,inferSchema=True)
sip_installments.display()

# COMMAND ----------

sip_registrations = spark.read.csv("/Volumes/wealth_catalog/raw_zone/transaction/sip_registrations.csv",header=True,inferSchema=True)
sip_registrations.display()

# COMMAND ----------

folios = spark.read.csv( "/Volumes/wealth_catalog/raw_zone/transaction/folios.csv",header=True,inferSchema=True)
folios.display()

# COMMAND ----------

clients = spark.read.csv("/Volumes/wealth_catalog/raw_zone/client/clients.csv",header=True,inferSchema=True)
clients.display()

# COMMAND ----------

advisors = spark.read.csv("/Volumes/wealth_catalog/raw_zone/advisor/advisors.csv",header=True,inferSchema=True)
advisors.display()

# COMMAND ----------

fact_sip_installments_registration = sip_installments.join( sip_registrations, "sip_id", "left")
fact_sip_installments_registration.display()

# COMMAND ----------

fact_sip_installments_folio = fact_sip_installments_registration.join(folios,"folio_id","left")
fact_sip_installments_folio.display()

# COMMAND ----------

fact_sip_installments_client = fact_sip_installments_folio.join(clients,"client_id","left")
fact_sip_installments_client.display()

# COMMAND ----------

fact_sip_installments_advisor = fact_sip_installments_client.join(advisors,"advisor_id","left")
fact_sip_installments_advisor.display()

# COMMAND ----------

dim_client = spark.table("wealth_catalog.warehouse.dim_client")
dim_client.display()

# COMMAND ----------

dim_advisor = spark.table("wealth_catalog.warehouse.dim_advisor")
dim_advisor.display()

# COMMAND ----------

dim_scheme = spark.table( "wealth_catalog.warehouse.dim_scheme")
dim_scheme.display()

# COMMAND ----------

dim_time = spark.table("wealth_catalog.warehouse.dim_time")
dim_time.display()

# COMMAND ----------

from pyspark.sql.functions import col, to_date
fact_sip_installments_date_key = fact_sip_installments_advisor.join(dim_time.select("full_date","date_key"),to_date(col("installment_date")) == col("full_date"),"left")
fact_sip_installments_date_key.display()

# COMMAND ----------

fact_sip_installments_final = fact_sip_installments_date_key.select("installment_id", "sip_id","client_id", "advisor_id", "scheme_id","date_key","amount", "units","nav")
fact_sip_installments_final.display()

# COMMAND ----------

fact_sip_installments_final.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("wealth_catalog.warehouse.fact_sip_installments")

# COMMAND ----------


spark.sql("""SELECT * FROM wealth_catalog.warehouse.fact_sip_installments""").display()