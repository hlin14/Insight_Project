import sys
#sys.path.append("./helper/")
#sys.path.insert(0, './helper/')
import sys
import pyspark
import json
#import helper
import math
from datetime import datetime, timedelta

class BatchTransformer:
    def __init__(self):
	self.sc = pyspark.SparkContext.getOrCreate()
    
    def read_data_from_s3(self):
	s3_path = "s3a://han-ping-insight-bucket/nyc_taxi_raw_data/yellow/trip_data_2017_04_example.csv"
	self.data = self.sc.textFile(s3_path)
	#ignore the first row
	header = self.data.first() #extract header
	self.data = self.data.filter(lambda row: row != header) 

    def do_transform(self):
	self.data = (self.data
			.map(lambda x: x.split(','))
			#add rounded_time col
			.map(lambda x: [x[0], x[1], x[2], x[3],x[4], datetime.strptime(x[0], "%Y/%m/%d %H:%M") - timedelta(minutes = datetime.strptime(x[0], "%Y/%m/%d %H:%M").minute % 10)])

			#add rounded_longtitude_col, #add rounded_latitude_col
			.map(lambda x: [x[0], x[1], x[2], x[3],x[4], x[5], math.floor(float(x[2]) * 10000) / 10000.0, math.floor(float(x[3]) * 10000) / 10000.0])
	#cal count for all (time, long, lat), add the col of "count"

	#cal all near time,long, lat, find out the highest count, and add the (long, lat) in the "recoomand" col
			)

    def save_to_postgresql(self):
	pass

if __name__ == '__main__':
    transformer = BatchTransformer()
    
    transformer.read_data_from_s3()
    transformer.do_transform()
    print transformer.data.take(14)
    print "================"

