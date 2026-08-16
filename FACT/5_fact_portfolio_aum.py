# Databricks notebook source
transactions = spark.read.csv("/Volumes/wealth_catalog/raw_zone/transaction/transactions.csv", header=True, inferSchema=True)
transactions.display()

# COMMAND ----------



# COMMAND ----------

folios = spark.read.csv("/Volumes/wealth_catalog/raw_zone/transaction/folios.csv", header=True, inferSchema=True)
folios.display()

# COMMAND ----------

clients = spark.read.csv("/Volumes/wealth_catalog/raw_zone/client/clients.csv", header=True, inferSchema=True)
clients.display()

# COMMAND ----------

advisors = spark.read.csv("/Volumes/wealth_catalog/raw_zone/advisor/advisors.csv", header=True, inferSchema=True)
advisors.display()

# COMMAND ----------

nav_history = spark.read.csv("/Volumes/wealth_catalog/raw_zone/nav/nav_history.csv", header=True, inferSchema=True)
nav_history.display()

# COMMAND ----------

schemes = spark.read.csv("/Volumes/wealth_catalog/raw_zone/scheme/schemes.csv", header=True, inferSchema=True)
schemes.display()

# COMMAND ----------

dim_time = spark.table("wealth_catalog.warehouse.dim_time")
dim_time.display()

# COMMAND ----------

transactions.columns


# COMMAND ----------

folios.columns
clients.columns
advisors.columns
schemes.columns
#nav_history.columns

# COMMAND ----------

fact_aum_folio = transactions.join(folios, "folio_id", "left")
fact_aum_folio.display()

# COMMAND ----------

fact_aum_client = fact_aum_folio.join(clients, "client_id", "left")
fact_aum_client.display()

# COMMAND ----------

fact_aum_advisor = fact_aum_client.join(advisors, "advisor_id", "left")
fact_aum_advisor.display()

# COMMAND ----------

fact_aum_scheme = fact_aum_advisor.join(schemes, "scheme_id", "left")
fact_aum_scheme.display()

# COMMAND ----------

fact_aum_nav = fact_aum_scheme.join(nav_history, "scheme_id", "left")
fact_aum_nav.display()

# COMMAND ----------

transactions_v2 = spark.read.csv("/Volumes/wealth_catalog/raw_zone/transaction/transactions_v2.csv", header=True, inferSchema=True)
transactions_v2.display()

# COMMAND ----------

fact_aum_folio = transactions_v2.join(folios, "folio_id", "left").display()

# COMMAND ----------

from pyspark.sql.functions import col, to_date

fact_aum_date_key = fact_aum_nav.join(dim_time.select("full_date","date_key"),to_date(col("created_date")) == col("full_date"),"left")

fact_aum_date_key.display()

# COMMAND ----------

fact_aum_folio = transactions_v2.join(folios, "folio_id", "left")
fact_aum_folio.display()

# COMMAND ----------

fact_aum_client = fact_aum_folio.join(clients, "client_id", "left")
fact_aum_client.display()

# COMMAND ----------

fact_aum_advisor = fact_aum_client.join(advisors, "advisor_id", "left")
fact_aum_advisor.display()

# COMMAND ----------

fact_aum_scheme = fact_aum_advisor.join(schemes, "scheme_id", "left")
fact_aum_scheme.display()

# COMMAND ----------

fact_aum_nav = fact_aum_scheme.join(nav_history, "scheme_id", "left")
fact_aum_nav.display()

# COMMAND ----------

from pyspark.sql.functions import col, to_date
fact_aum_date_key = fact_aum_nav.join(dim_time.select("full_date","date_key"),to_date(col("transaction_date")) == col("full_date"),"left")
fact_aum_units = fact_aum_date_key.withColumn("units_held", col("units"))
fact_aum_units.display()

# COMMAND ----------

fact_aum_date_key = fact_aum_date_key.drop(nav_history["nav"])

# COMMAND ----------

from pyspark.sql.functions import col

fact_aum_calc = fact_aum_date_key.withColumn("units_held", col("units"))
fact_aum_calc.display()

# COMMAND ----------

fact_aum_calc = fact_aum_calc.withColumn("latest_nav", col("nav"))
fact_aum_calc.display()

# COMMAND ----------

fact_aum_calc = fact_aum_calc.withColumn("market_value", col("units_held") * col("latest_nav"))
fact_aum_calc.display()

# COMMAND ----------

fact_aum_calc = fact_aum_calc.withColumn("cost_value", col("amount"))
fact_aum_calc.display()

# COMMAND ----------

#from pyspark.sql.functions import col
#fact_aum_calc = fact_aum_calc.withColumn("cost_value", col("units_held") * col("nav"))
#fact_aum_calc.display()

# COMMAND ----------

fact_aum_calc = fact_aum_calc.withColumn("gain_loss", col("market_value") - col("cost_value"))
fact_aum_calc.display()

# COMMAND ----------

fact_portfolio_aum = fact_aum_calc.select(
    "client_id",
    "advisor_id",
    "scheme_id",
    "date_key",
    "units_held",
    "latest_nav",
    "market_value",
    "cost_value",
    "gain_loss"
)

fact_portfolio_aum.display()

# COMMAND ----------

fact_portfolio_aum.selectExpr(
    "min(gain_loss) as min_gain_loss",
    "max(gain_loss) as max_gain_loss",
    "avg(gain_loss) as avg_gain_loss"
).display()

# COMMAND ----------

fact_portfolio_aum.filter(col("latest_nav").isNull()).count()

# COMMAND ----------

fact_portfolio_aum.write.format("delta").mode("overwrite").option("overwriteSchema","true").saveAsTable("wealth_catalog.warehouse.fact_portfolio_aum")

# COMMAND ----------

spark.table("wealth_catalog.warehouse.fact_portfolio_aum").display()