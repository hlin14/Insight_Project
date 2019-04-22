package com.insight;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.node.JsonNodeFactory;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.common.serialization.Deserializer;
import org.apache.kafka.common.serialization.Serde;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.common.serialization.Serializer;
import org.apache.kafka.connect.json.JsonDeserializer;
import org.apache.kafka.connect.json.JsonSerializer;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.kstream.KStream;
import org.apache.kafka.streams.kstream.KStreamBuilder;
import org.apache.kafka.streams.kstream.KTable;

import java.time.Instant;
import java.util.Properties;

public class core {

    public static void main(String[] args) {
        Properties config = new Properties();

        config.put(StreamsConfig.APPLICATION_ID_CONFIG, "insight-bus-application");
        config.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "127.0.0.1:9092");
//        config.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");

        config.put(StreamsConfig.CACHE_MAX_BYTES_BUFFERING_CONFIG, "0");

        config.put(StreamsConfig.PROCESSING_GUARANTEE_CONFIG, StreamsConfig.EXACTLY_ONCE);

        // json Serde
        final Serializer<JsonNode> jsonSerializer = new JsonSerializer();
        final Deserializer<JsonNode> jsonDeserializer = new JsonDeserializer();
        final Serde<JsonNode> jsonSerde = Serdes.serdeFrom(jsonSerializer, jsonDeserializer);


        KStreamBuilder builder = new KStreamBuilder();

        KStream<String, JsonNode> busStream =
                builder.stream(Serdes.String(), jsonSerde, "bus-stream-topic");

	//change key
	KStream<String, JsonNode> busStreamChangeKey = busStream
		.selectKey((key, transaction)-> transaction.get("busID").asText());

	//peek
//	KStream<String, JsonNode> unchangeStream = busStreamChangeKey
//	.peek((key, transaction)->System.out.println(key+","+transaction));


	//stream to do map value of dur_distance, dur_time, ave_speed

	//write to bus-table-topic
	busStreamChangeKey.to(Serdes.String(), jsonSerde, "bus-table-topic");


	//read by Ktable
        KTable<String, JsonNode> finalTable = builder.table(Serdes.String(), jsonSerde,"bus-table-topic");
	//send to final topic
       finalTable.to(Serdes.String(), jsonSerde, "busfinaltopic");




        KafkaStreams streams = new KafkaStreams(builder, config);
        streams.cleanUp();
        streams.start();

        // print the topology
        System.out.println(streams.toString());

        // shutdown hook to correctly close the streams application
        Runtime.getRuntime().addShutdownHook(new Thread(streams::close));
    }

}
