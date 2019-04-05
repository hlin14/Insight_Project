from kafka import KafkaConsumer
import psycopg2
import os
from datetime import datetime
import random
def start_consumer():
	#consumer = KafkaConsumer("taxi-stream-output", auto_offset_reset ='earliest')
	consumer = KafkaConsumer("taxi-stream-output")
	_id = 1
	for msg in consumer:

		print msg

		#connect to db, and save to db
		postgres_password = os.environ["POSTGRESPASSWORD"]
		conn_string = "host='10.0.0.10' dbname='ping_db' user='ping' password=" + postgres_password

		conn = psycopg2.connect(conn_string)

		cur = conn.cursor()
		dt = datetime(2015, 1, 1, 12, 30, 59, 0)
		#need try catch, id choice
		_id = random.randint(1,10001)
		cur.execute("INSERT INTO bus_testing VALUES (%s, 12 , 12, -74.1715, 40.6894, %s, 40.6895);",[_id, dt])
		conn.commit()
		cur.close()
		conn.close()
		#if using select * from ...
		#records = cursor.fetchall()



if __name__ == '__main__':
	start_consumer()
