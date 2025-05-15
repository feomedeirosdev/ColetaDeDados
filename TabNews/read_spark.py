# %%
from pyspark.sql import SparkSession
import os
os.environ["JAVA_HOME"] = "/home/medeiros/anaconda3/envs/dc_env"


# %%
spark = (SparkSession.builder
                     .appName("Python Spark SQL basic example")
                     .config("spark.some.config.option", "some-value")
                     .getOrCreate())

print(spark.version)
# %%
df = spark.read.option("pathGlobFilter", "*.json").json('/home/medeiros/Área de trabalho/TrilhaML/5_ColetaDeDados/ColetaDeDados/datas/epsodios/json/')

# %%
df.show()
# %%
