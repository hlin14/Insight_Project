from kafka import KafkaConsumer
consumer = KafkaConsumer("taxi-stream-output", auto_offset_reset ='earliest')
for msg in consumer:
    print msg
