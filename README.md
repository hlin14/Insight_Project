# Insight_Project
## Project Idea:
Making a real-time tracking system using Confluent Kafka on NYC bus dataset. 

## Demo:
Video:https://www.youtube.com/watch?v=InkbHj9vZDw
![alt text](https://github.com/hlin14/Insight_Project/blob/master/figures/demo_screen.png)
## Tech Stack: 
Kafka, Cassandra, Flask
![alt text](https://github.com/hlin14/Insight_Project/blob/master/figures/tech_stack.png)


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


