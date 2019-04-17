package com.insight;

import com.fasterxml.jackson.databind.node.JsonNodeFactory;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringSerializer;

import java.time.Instant;
import java.util.Properties;
import java.util.concurrent.ThreadLocalRandom;
import java.util.UUID;
import java.time.Duration;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

import java.util.HashMap;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

public class producer {
    public static void main(String[] args) {
        Properties properties = new Properties();

        // kafka bootstrap server
        properties.setProperty(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "127.0.0.1:9092");
        properties.setProperty(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        properties.setProperty(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        properties.setProperty(ProducerConfig.ACKS_CONFIG, "all"); 
        properties.setProperty(ProducerConfig.RETRIES_CONFIG, "3");
        properties.setProperty(ProducerConfig.LINGER_MS_CONFIG, "1");
        properties.setProperty(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, "true");

        Producer<String, String> producer = new KafkaProducer<>(properties);
        int batchNum = 0;

        while (true) {
            int i = 0;
            System.out.println("Producing batch: " + batchNum);
            batchNum += 1;
            //init HaspMap
            HashMap<Integer, LocalDateTime> durTMap= new HashMap<Integer, LocalDateTime>();
            HashMap<Integer, Double> durDMap= new HashMap<Integer, Double>();

            String csvFile = "MTA-Bus-Time-2014-08-01_small_csv.csv";
            BufferedReader br = null;
            String line = "";
            String cvsSplitBy = ",";

            try {
                br = new BufferedReader(new FileReader(csvFile));
                while ((line = br.readLine()) != null) {

                    String[] transaction = line.split(cvsSplitBy);

                    if (i > 0) {
                        try {
                            //get data from the columns
                            Double latitude = Double.valueOf(transaction[0]);
                            Double longtitude = Double.valueOf(transaction[1]);
                            String timeReceived = transaction[2];
                            Integer busID = Integer.parseInt(transaction[3]);
                            Double distanceAlong = Double.valueOf(transaction[4]);
                            Integer directionID = Integer.parseInt(transaction[5]);
                            String phase = transaction[6];
                            String routeID = transaction[7];
                            Double nextStopDistance = Double.valueOf(transaction[9]);
                            String nextStopID = transaction[10];

                            //tranform time to localdatetime
                            DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy/M/d H:mm");
                            LocalDateTime formatDateTime = LocalDateTime.parse(timeReceived, formatter);

                            producer.send(newTransaction(latitude, longtitude, formatDateTime, busID, distanceAlong, directionID, phase, routeID, nextStopDistance, nextStopID));


                            Thread.sleep(100);
                            //producer.close();
                            //producer.send(newTransaction(40.713702, -73.97967, 3928, 3974.805808, 0, "LAYOVER_DURING", "MTA NYCT_M22", 129.3308986, "MTA_903025"));
                            //Thread.sleep(100);
                            //i += 1;
                        } catch (InterruptedException e) {
                            break;
                        }
                    }
                    i += 1;
                }
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            } finally {
                if (br != null) {
                    try {
                        br.close();
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
            }
        //producer.close();
        }
    //producer.close();
    }

    public static ProducerRecord<String, String> newTransaction(Double latitude, Double longtitude, LocalDateTime formatDateTime, Integer busID, Double distanceAlong, Integer directionID, String phase, String routeID, Double nextStopDistance, String nextStopID) {
        // creates an empty json {}
        ObjectNode transaction = JsonNodeFactory.instance.objectNode();

        UUID uuid = UUID.randomUUID();
        String uniqueID = uuid.toString();
        // Instant.now() is to get the current time using Java 8
        //Instant now = Instant.now();

        transaction.put("latitude", latitude);
        transaction.put("longtitude", longtitude);
        transaction.put("timeReceived", formatDateTime.toString());
        transaction.put("busID", busID);
        transaction.put("distanceAlong", distanceAlong);
        transaction.put("directionID", directionID);
        transaction.put("phase", phase);
        transaction.put("routeID", routeID);
        transaction.put("nextStopDistance", nextStopDistance);
        transaction.put("nextStopID", nextStopID);

        return new ProducerRecord<>("bus-stream-topic", uniqueID, transaction.toString());
    }
}
