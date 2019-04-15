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
            try {
                producer.send(newTransaction(40.668602, -73.986697, 469, 4135.347107, 1, "IN_PROGRESS", "MTA NYCT_B63", 2.631838042, "MTA_305423"));
                Thread.sleep(100);
                producer.send(newTransaction(40.713702, -73.97967, 3928, 3974.805808, 0, "LAYOVER_DURING", "MTA NYCT_M22", 129.3308986, "MTA_903025"));
                Thread.sleep(100);
                i += 1;
            } catch (InterruptedException e) {
                break;
            }
        }
        producer.close();
    }

    public static ProducerRecord<String, String> newTransaction(Double latitude, Double longtitude, Integer busID, Double distanceAlong, Integer directionID, String phase, String routeID, Double nextStopDistance, String nextStopID) {
        // creates an empty json {}
        ObjectNode transaction = JsonNodeFactory.instance.objectNode();

	UUID uuid = UUID.randomUUID();
	String uniqueID = uuid.toString();
        // Instant.now() is to get the current time using Java 8
        Instant now = Instant.now();

        transaction.put("latitude", latitude);
        transaction.put("longtitude", longtitude);
        transaction.put("time", now.toString());
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
