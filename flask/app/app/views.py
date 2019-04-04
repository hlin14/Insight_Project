from app import app
import psycopg2

from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

import os
def connect_to_db():
    conn_string = "host='10.0.0.10' dbname='ping_db' user='ping' password='a126583372'"

    conn = psycopg2.connect(conn_string)

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM result_to_flask")
    current = ""
    recommend = ""
    records = cursor.fetchall()
    
    return records
    #return str(records[0])

@app.route('/')
@app.route('/index')
def index():
    #print records
    records = connect_to_db()
    client1 = {
		"id":records[0][0],
		"cur_long":float(records[0][1]),
		"cur_lat":float(records[0][2]),
		"rec_long":float(records[0][3]),
		"rec_lat":float(records[0][4])
		}
    #return conn_string	
    #return "Hello, World!"
    GOOGLEMAPAPI = os.environ["GOOGLEMAPAPI"]
    return render_template('example2.html', googleapi = GOOGLEMAPAPI, client1 = client1)
