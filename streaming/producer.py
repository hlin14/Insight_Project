from kafka import KafkaProducer
from json import dumps


producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda x: dumps(x).encode('utf-8'))

for e in range(10):
    data = "a"
    producer.send('taxi-stream-input', value=data)
    producer.flush()
