from kafka import KafkaConsumer
import psycopg2

def start_consumer():
	consumer = KafkaConsumer("taxi-stream-output", auto_offset_reset ='earliest')

	for msg in consumer:

		print msg

		#connect to db, and save to db
		postgres_password = os.environ["POSTGRESPASSWORD"]
		conn_string = "host='10.0.0.10' dbname='ping_db' user='ping' password=" + postgres_password

		conn = psycopg2.connect(conn_string)

		cursor = conn.cursor()

		#cursor.execute("INSERT INTO bus_testing VALUES (1, 5, 30, -74.1715, 40.6894, -74.1716, 40.6895);")

		#if using select * from ...
		#records = cursor.fetchall()



if __name__ == '__main__':
	start_consumer()
