from kafka import KafkaConsumer
import ast
from cassandra.cluster import Cluster
import json

def start_consumer():

	cluster = Cluster()
	session = cluster.connect("test2")

	consumer = KafkaConsumer("busfinaltopic")
	for msg in consumer:
		if msg.value != "":
			print msg.value
			try: 
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
			except ValueError as error:
				print("invalid json: %s" % error)

if __name__ == '__main__':
	start_consumer()
