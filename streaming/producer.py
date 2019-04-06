from kafka import KafkaProducer
from json import dumps
import boto3
import lazyreader
import time

def get_s3_and_produce():
	producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda x: dumps(x).encode('utf-8'))
	while True:
		s3 = boto3.client('s3')
		obj = s3.get_object(Bucket="han-ping-insight-bucket", Key="nyc_taxi_raw_data/STREAMING_FILE/MTA-Bus-Time-2014-08-01.csv")
		for line in lazyreader.lazyread(obj['Body'], delimiter='\n'):
			#print line
			message = line.strip()
			message = message.split(",")
			print message
			#need to filter out the col 
			produce(message, producer)
			time.sleep(0.01)

def produce(msg, producer):


	producer.send('word-count-input', value=msg)
	producer.flush()


if __name__ == '__main__':
	get_s3_and_produce()

