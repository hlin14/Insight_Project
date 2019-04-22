
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
		
		print json_sent
		socketio.emit('my response', json_sent)
		socketio.sleep(5)



@app.route('/',methods=['GET', 'POST'])
@app.route('/index',methods=['GET', 'POST'])
def index():
	connect_to_cassandra()

	GOOGLEMAPAPI = os.environ["GOOGLEMAPAPI"]
	return render_template('example2.html', googleapi = GOOGLEMAPAPI)

def messageReceived(methods=['GET', 'POST']):
	print 'message was received!'

if __name__ == '__main__':

	socketio.run(app, host='0.0.0.0', debug = True)
