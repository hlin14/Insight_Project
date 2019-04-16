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

        int i = 0;
        while (true) {
            System.out.println("Producing batch: " + i);
            //init HaspMap
            HashMap<Integer, LocalDateTime> durTMap= new HashMap<Integer, LocalDateTime>();
            HashMap<Integer, Double> durDMap= new HashMap<Integer, Double>();




            try {
                Double latitude = 40.668602;
                Double longtitude = -73.986697;
                String timeReceived = "2014/8/1 4:00";
                Integer busID = 469;
                Double distanceAlong = 4135.347107;
                Integer directionID = 1;
                String phase = "IN_PROGRESS";
                String routeID = "MTA NYCT_B63";
                Double nextStopDistance = 2.631838042;
                String nextStopID = "MTA_305423";

                //tranform time to localdatetime
                DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy/M/d H:mm");
                LocalDateTime formatDateTime = LocalDateTime.parse(timeReceived, formatter);

                //init duration time(sec) and distance(meter)
                Long durT = 0L;
                Double durD = 0.0;

                if (phase.equals("IN_PROGRESS")){
                    //update duration time
                    if (!durTMap.containsKey(busID)) {
                        durTMap.put(busID, formatDateTime);
                    }
                    else {
                        LocalDateTime lastFormatDateTime=durTMap.get(busID);
                        Duration duration = Duration.between(lastFormatDateTime, formatDateTime);
                        Long durSec = duration.getSeconds();
                        //make sure the time is correct
                        if (durSec > 0) {
                            durT = durSec;
                        }
                    }

                    //update duration distance
                    if (!durDMap.containsKey(busID)) {
                        durDMap.put(busID, distanceAlong);
                    }
                    else {
                        Double lastDistanceAlong = durDMap.get(busID);
                        Double durDis = distanceAlong - lastDistanceAlong;
                        //make sure duration distance is correct
                        if (durDis > 0) {
                            durD = durDis;
                        }
                    }

                }

                producer.send(newTransaction(latitude, longtitude, formatDateTime, busID, distanceAlong, directionID, phase, routeID, nextStopDistance, nextStopID, durT, durD));
                Thread.sleep(100);
                //producer.send(newTransaction(40.713702, -73.97967, 3928, 3974.805808, 0, "LAYOVER_DURING", "MTA NYCT_M22", 129.3308986, "MTA_903025"));
                //Thread.sleep(100);
                i += 1;
            } catch (InterruptedException e) {
                break;
            }
        }
        producer.close();
    }

    public static ProducerRecord<String, String> newTransaction(Double latitude, Double longtitude, LocalDateTime formatDateTime, Integer busID, Double distanceAlong, Integer directionID, String phase, String routeID, Double nextStopDistance, String nextStopID, Long durT, Double durD) {
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
        transaction.put("durT", durT);
        transaction.put("durD", durD);

        return new ProducerRecord<>("bus-stream-topic", uniqueID, transaction.toString());
    }
}
