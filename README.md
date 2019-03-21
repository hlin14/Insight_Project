# Insight_Project
## Project Idea:
Making a real-time analytics using Kafka stream, Flink streaming on NYC taxi dataset. Estimate the direction that an empty taxi can get a higher chance to have a customer. Reconstruct/Simplied the architecture with previous fellow's taxi-optimizer project, also benchmark and analyze the tradeoff.

## Tech Stack: 
Kafka, Flink Streaming, Airflow
## Data Source:
NYC taxi trip data, including the total amount of money paid and where, when the taxi driver pick up the customer
## Engineering Challenge:
  1. Provide suggestions to the taxi drivers where will get the highest paid and the least expected waited time.
  2. Implement Flink and Kafka streaming. Benchmark with latency, throughput, fault tolerance, memory usage
  3. Ingest different source of dataset.
## Business Value:
  1. Less empty taxi, congestion control on traffic. More expected revenue for taxi drivers, less expected waited time for the customers.
  2. Using only Kafka will simplfied the architecture. 
  3. Using Kafka and Flink will provide less latency for the users than using Spark.
## MVP:
Same functionality of taxi-optimzer but using Kafka and Flink
## Stretch Goals:
  1. Provide more functionlity to the taxi-optimizer
  2. More dataset from uber, lyft
