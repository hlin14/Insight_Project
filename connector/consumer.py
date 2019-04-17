from kafka import KafkaConsumer
import ast
from cassandra.cluster import Cluster
import json

def start_consumer():

	cluster = Cluster()
	session = cluster.connect("test2")

	#rows = session.execute('select * from kafka_connect_offsets;')
	#session.execute("update forcas10222 set name='john', age='6' where id='1'")
	#for row in rows:
	#	print row

	consumer = KafkaConsumer("bus-final-topic", auto_offset_reset ='earliest')
	for msg in consumer:
		if msg.value != "":
			print msg.value
			transaction = json.loads(msg.value)
			session.execute("update bustable set latitude=%s, longitude=%s, nextstopdistance=%s, nextstopid=%s, phase=%s, routeid=%s, timereceived=%s where busid=%s", (
			str(transaction["latitude"]),
			str(transaction["longtitude"]),
			str(transaction["nextStopDistance"]),
			transaction["nextStopID"],
			transaction["phase"],
			transaction["routeID"],
			transaction["timeReceived"],
			transaction["busID"]
			))
			#print transaction["busID"]
			#print type(msg.value)
			#msg = ast.literal_eval(msg.value)
			#print msg[0]

if __name__ == '__main__':
	start_consumer()
