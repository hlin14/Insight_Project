import sys
import pyspark

class BatchTransformer:
    def __init__(self):
	self.sc = pyspark.SparkContext.getOrCreate()
	self.data = ""
    def read_data_from_s3(self):
	s3_path = "s3a://han-ping-insight-bucket/nyc_taxi_raw_data/yellow/trip_data_2017_04.csv"
	self.data = self.sc.textFile(s3_path)
if __name__ == '__main__':
    transformer = BatchTransformer()
    transformer.read_data_from_s3()
    print transformer.data.take(10)

