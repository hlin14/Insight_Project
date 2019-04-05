from kafka import KafkaConsumer
import psycopg2
import os
from datetime import datetime
import random
import ast
import uuid
def start_consumer():
	#consumer = KafkaConsumer("taxi-stream-output", auto_offset_reset ='earliest')
	consumer = KafkaConsumer("taxi-stream-output")
	_id = 0
	for msg in consumer:

		msg = ast.literal_eval(msg.value)
		#print msg
		#connect to db, and save to db
		postgres_password = os.environ["POSTGRESPASSWORD"]
		conn_string = "host='10.0.0.10' dbname='ping_db' user='ping' password=" + postgres_password

		conn = psycopg2.connect(conn_string)

		cur = conn.cursor()
		#dt = datetime(2015, 1, 1, 12, 30, 59, 0)
		#need try catch, id choice
		if _id != 0:
			cur.execute("INSERT INTO bus_testing VALUES (%s, %s , %s, %s, %s, %s, %s);",[_id, msg[7], msg[3], msg[1], msg[0],msg[2], msg[4]])
		_id = str(uuid.uuid4())
		conn.commit()
		cur.close()
		conn.close()
		#if using select * from ...
		#records = cursor.fetchall()



if __name__ == '__main__':
	start_consumer()
