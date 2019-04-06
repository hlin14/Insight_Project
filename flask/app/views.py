from app import app
import psycopg2

from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

import os
def connect_to_db():
	postgres_password = os.environ["POSTGRESPASSWORD"]
	conn_string = "host='10.0.0.10' dbname='ping_db' user='ping' password=" + postgres_password

	conn = psycopg2.connect(conn_string)

	cursor = conn.cursor()

	cursor.execute("SELECT * FROM bus_testing WHERE bus_id = %s ORDER BY date_time DESC LIMIT 1;",[5945])
	records = cursor.fetchall()
	print records
	return records
	#return str(records[0])

@app.route('/')
@app.route('/index')
def index():
	records = connect_to_db()

	client1 = {
		"id":1,
		"cur_long":float(records[0][3]),
		"cur_lat":float(records[0][4]),
		"rec_long":-73.98418,
		"rec_lat":40.748222
		}

	GOOGLEMAPAPI = os.environ["GOOGLEMAPAPI"]
	return render_template('example2.html', googleapi = GOOGLEMAPAPI, client1 = client1)
