# Databricks notebook source

from pyspark.sql.functions import *
dim_time = spark.sql("""SELECT explode(sequence(to_date('2020-01-01'),to_date('2035-12-31'),interval 1 day)) AS full_date""")
dim_time.display()

# COMMAND ----------

from pyspark.sql.functions import monotonically_increasing_id

dim_time = (
    dim_time
    .withColumn("date_key", monotonically_increasing_id())
    .withColumn("day", dayofmonth("full_date"))
    .withColumn("month", month("full_date"))
    .withColumn("month_name", date_format("full_date","MMMM"))
    .withColumn("quarter", quarter("full_date"))
    .withColumn("year", year("full_date"))
    .withColumn(
        "financial_year",
        when(month("full_date") >= 4,
             concat(year("full_date"), lit("-"), year("full_date")+1))
        .otherwise(
             concat(year("full_date")-1, lit("-"), year("full_date")))
    ))

# COMMAND ----------

dim_time = dim_time.select("date_key","full_date","day","month", "month_name","quarter", "year","financial_year")
dim_time.display()

# COMMAND ----------

dim_time.write.format("delta").mode("overwrite").option("overwriteSchema","true").saveAsTable("wealth_catalog.warehouse.dim_time")

# COMMAND ----------

spark.table("wealth_catalog.warehouse.dim_time").display()