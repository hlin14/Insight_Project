import psycopg2

from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

import os

from flask_socketio import SocketIO
import threading

from cassandra.cluster import Cluster

app = Flask(__name__)
socketio = SocketIO(app)

def connect_to_cassandra():
        cluster = Cluster(["127.0.0.1"],port=9042)
        session = cluster.connect('test2')

        query_prepare = session.prepare('SELECT * FROM bustable;')
	global query_prepare, session



@socketio.on('my event')
def catch_event(json, methods=['GET', 'POST']):
	print json
	while True:
		#print json
		
		json_sent = []
		rows = session.execute(query_prepare)
		for row in rows:
			json_sent.append({"busID":row[0], "long":float(row[2]), "lat":float(row[1])})
			#print row[0], row[1], row[2]
		
		#json_sent = {"long": float(ret_long),"lat": float(ret_lat)}
		#json_sent = [{"busID":123, "long":123, "lat":456},{"busID":456, "long":123, "lat":456}]
		print json_sent
		socketio.emit('my response', json_sent)
		socketio.sleep(10)


def connect_to_db():
	postgres_password = os.environ["POSTGRESPASSWORD"]
	conn_string = "host='10.0.0.10' dbname='ping_db' user='ping' password=" + postgres_password

	conn = psycopg2.connect(conn_string)

	cursor = conn.cursor()
	global cursor
	#cursor.execute("SELECT * FROM bus_testing WHERE bus_id = %s ORDER BY date_time DESC LIMIT 1;",[5945])
	#records = cursor.fetchall()
	#print records
	#return records
	#return str(records[0])

@app.route('/',methods=['GET', 'POST'])
@app.route('/index',methods=['GET', 'POST'])
def index():
#	connect_to_db()
	connect_to_cassandra()
#	client1 = {
#		"id":1,
#		"cur_long":float(records[0][3]),
#		"cur_lat":float(records[0][4]),
#		"rec_long":-73.98418,
#		"rec_lat":40.748222
#		}

	GOOGLEMAPAPI = os.environ["GOOGLEMAPAPI"]
	return render_template('example2.html', googleapi = GOOGLEMAPAPI)

def messageReceived(methods=['GET', 'POST']):
	print 'message was received!'
'''
@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
	print 'received my event: ' + str(json)
	#print json['message']
	
	global cursor
	cursor.execute("SELECT * FROM bus_testing WHERE bus_id = %s ORDER BY date_time DESC LIMIT 1;",[float(json['message'])])
	records = cursor.fetchall()

	json = {
		"long": float(records[0][3]),
		"lat": float(records[0][4])
	}	


	socketio.emit('my response', json, callback=messageReceived)
'''

'''
q = []
@socketio.on('my event')
def set_interval(json, methods=['GET', 'POST']):
        if  "" != json.get('message', ""):
		q.append(json)
                t = threading.Thread(target=func)
                t.start()
        else:

                func()

'''

#@socketio.on('my event')
def func(json, methods=['GET', 'POST']):
	while True:
#		json = q[-1]
		print 'received my event: ' + str(json)
		#print json['message']

		global cursor
		cursor.execute("SELECT * FROM bus_testing WHERE bus_id = %s ORDER BY date_time DESC LIMIT 1;",[float(json['message'])])
		records = cursor.fetchall()

		json_sent = {
			"long": float(records[0][3]),
			"lat": float(records[0][4])
		}

		print json_sent
		socketio.emit('my response', json_sent)
		socketio.sleep(0.8)
if __name__ == '__main__':

	socketio.run(app, host='0.0.0.0', debug = True)
