# Databricks notebook source
redemption_transactions = spark.read.csv("/Volumes/wealth_catalog/raw_zone/transaction/redemption_transactions.csv",header=True,inferSchema=True)
redemption_transactions.display()

# COMMAND ----------

folios = spark.read.csv("/Volumes/wealth_catalog/raw_zone/transaction/folios.csv",header=True,inferSchema=True)
folios.display()

# COMMAND ----------

dim_advisor = spark.table("wealth_catalog.warehouse.dim_advisor")

dim_advisor.display()

# COMMAND ----------

dim_client = spark.table("wealth_catalog.warehouse.dim_client")

dim_client.display()

# COMMAND ----------

transactions_v2 = spark.read.csv("/Volumes/wealth_catalog/raw_zone/transaction/transactions_v2.csv",header=True,inferSchema=True)

transactions_v2.display()

# COMMAND ----------

dim_time = spark.table("wealth_catalog.warehouse.dim_time")

dim_time.display()

# COMMAND ----------

dim_scheme = spark.table("wealth_catalog.warehouse.dim_scheme")

dim_scheme.display()

# COMMAND ----------



# COMMAND ----------

#fact_transaction_nav = fact_redemption_nav.select( "folio_id", "scheme_id", "amount", "units", "nav")

#fact_transaction_nav.display()

# COMMAND ----------

#redemption_folio = redemption_transactions.join(folios,"folio_id","left")

#redemption_folio.display()

# COMMAND ----------

redemption_folio = redemption_transactions.join(folios, "folio_id", "left")

redemption_client = redemption_folio.join(
    dim_client,
    "client_id",
    "left")

redemption_client.display()

# COMMAND ----------

redemption_advisor = redemption_client.join(
    dim_advisor,
    "advisor_id",
    "left")

redemption_advisor.display()

# COMMAND ----------

redemption_scheme = redemption_advisor.join(
    dim_scheme,
    "scheme_id",
    "left"
)

redemption_scheme.display()

# COMMAND ----------

from pyspark.sql.functions import to_date, col

redemption_date = redemption_advisor.withColumn("redemption_date", to_date(col("redemption_date"), "yyyy-MM-dd"))

fact_redemption_time = redemption_date.join(dim_time,redemption_date["redemption_date"] == dim_time["full_date"],"left")
fact_redemption_time.display()

# COMMAND ----------

nav_data = transactions_v2.select(
    "folio_id",
    "scheme_id",
    "nav"
).dropDuplicates(["folio_id", "scheme_id"])

nav_data.display()

# COMMAND ----------

fact_redemption_time.select(
    "folio_id",
    "scheme_id"
).display()

# COMMAND ----------

transactions_v2.select(
    "folio_id",
    "scheme_id",
    "nav",
    "transaction_type",
    "transaction_date"
).display()

# COMMAND ----------

fact_redemptions_final = fact_redemption_time.drop("nav").crossJoin(
    transactions_v2.select("nav").limit(12000)
)

fact_redemptions_final.display()

# COMMAND ----------

fact_redemptions_final.count()

# COMMAND ----------

from pyspark.sql.window import Window
from pyspark.sql.functions import row_number

nav_data = transactions_v2.select("transaction_id", "nav") \
    .withColumn(
        "rn",
        row_number().over(Window.orderBy("transaction_id"))
    )

fact_redemptions_final = fact_redemption_time \
    .withColumn(
        "rn",
        row_number().over(Window.orderBy("redemption_id"))
    ) \
    .join(nav_data, "rn", "left") \
    .drop("rn", "transaction_id")

fact_redemptions_final.display()

# COMMAND ----------

fact_redemptions_final.drop("city").write \
.format("delta") \
.mode("overwrite") \
.option("overwriteSchema","true") \
.saveAsTable("wealth_catalog.warehouse.fact_redemptions")

# COMMAND ----------

spark.table("wealth_catalog.warehouse.fact_redemptions").display()