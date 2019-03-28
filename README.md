# Insight_Project
## Project Idea:
Making a real-time analytics using Kafka stream, Flink streaming on NYC taxi dataset. Estimate the direction that an empty taxi can get a higher chance to have a customer. Reconstruct/Simplied the architecture with previous fellow's taxi-optimizer project, also benchmark and analyze the tradeoff.

## Tech Stack: 
Spark streaming, Kafka streaming, PostgreSQL, Airflow, Flask
## Data Source:
NYC taxi trip data, including the total amount of money paid and where, when the taxi driver pick up the customer
## Engineering Challenge:
  1. Replace the original Architecture(Spark streaming) with Kafka streaming. Benchmark with latency, throughput, fault tolerance, memory usage
  2. Ingest different source of dataset.
  
  
## Running Existing Project

Original Architecture Schema
![alt text](https://github.com/AndreyBozhko/TaxiOptimizer/blob/master/docs/pipeline.jpg)

### Setting Up Environment
  1. peg_up.sh (done)
  2. copy_idrsapub_to_workers.sh (done)
  3. copy_allnodesdns_to_masters.sh (done)
  4. install_on_master.sh (done)
  5. install_all_node.sh (done)
  6. install and set up PostgreSQL on master of spark-stream-cluster (done)
  7. install and set up Airflow on master of spark-batch-cluster(working on)
  8. edit .config (for Kafka, PostgreSQl, S3 bucket)
 
### Running Taxi-Optimizer
  1. Run the generate_raw_data/generator_run.sh
  2. Schedule the batch job (airflow/schedule.sh)
  3. Start the streaming job (./spark-run.sh)
  4. Start the streaming messages with Kafka (./kafka -run --produce)
  5. Start Flask (flask/run.sh)


## Business Value:
  1. Less empty taxi, congestion control on traffic. More expected revenue for taxi drivers, less expected waited time for the customers.
  2. Using only Kafka will simplfied the architecture. 
  3. Using Kafka and Flink will provide less latency for the users than using Spark.
## MVP:
Same functionality of taxi-optimzer but using Kafka
## Stretch Goals:
  1. Provide more functionlity to the taxi-optimizer
  2. More dataset from uber, lyft
