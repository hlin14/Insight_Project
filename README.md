# Insight_Project
## Project Idea:
The motivation is to run a bus company in New York. In order to view all the current geolocations of the buses, I made a real-time geolocation tracking system using Confluent Kafka, Cassandra, Flask with Google Map API.

## Project Slides:
http://bit.ly/BusMap_slides

## Demo:
Video:http://bit.ly/BusMap_Demo
![alt text](https://github.com/hlin14/Insight_Project/blob/master/figures/demo_screen.png)
Description: The browser will update current location of the buses every second, the red marker represents the location, the numebr represents the bus_id. The red markers will automatically group into clusters to be more clear on the map. The color of the cluster represent the degree of density: red cluster means it contains more than 100 buses, yellow cluster means it contains more than 10 but less than 100 buses, blue cluster means it contains less than 10 buses. The detail can be shown by clicking the cluster or clicking the zoom-in button.

## Tech Stack: 
Kafka, Cassandra, Flask, AWS
![alt text](https://github.com/hlin14/Insight_Project/blob/master/figures/tech_stack.png)
I used a java program to be the producer of my Kafka cluster, and then I used Kafka Streams API to the transformation of the data, and used Ktable to be the final result in the topics. I choose Cassandra as my storeage because of its hight throughput. Then I use Flask with Google Map API to be my front-end.


## Data Source:
NYC bus trip data, including bus ID, time received, location, route ID, next stop distance(in meters), next stop ID.
(http://web.mta.info/developers/MTA-Bus-Time-historical-data.html)
Assuming every bus send location signal every second => 2000 transactions / sec.

  
## Setting Up Environment
Make sure running the zookeeper and kafka server before running the BusMap application.
Then, create three topics called "bus-stream-topic", "bus-table-topic", "busfinaltopic".
 
## Running BusMap
To run the program, need to run core kafka, producer, consumer and flask for front-end.
### Run the core kafka 
Go to kafka/producer/, first, build the jar file by running "mvn clean package", and then run the jar file by running "java -jar target/bus-core-1.0-SNAPSHOT-jar-with-dependencies.jar".
### Run the producer
Go to kafka/core/, first, build the jar file by running "mvn clean package", and then run the jar file by running "java -jar target/bus-producer-1.0-SNAPSHOT-jar-with-dependencies.jar".
### Run the consumer
Go to connector/, run "python consumer.py".
### Run the flask
Go to flask/app/ and run "python views.py".


