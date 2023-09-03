from confluent_kafka import Consumer, KafkaError
from confluent_kafka.schema_registry import SchemaRegistryClient, avro

# Kafka and Schema Registry configuration
kafka_conf = {
    'bootstrap.servers': 'localhost:9092',  # Replace with your broker addresses
    'group.id': 'my-consumer-group',
    'auto.offset.reset': 'earliest'
}

schema_registry_conf = {
    'url': 'http://localhost:8081'  # Replace with your Schema Registry URL
}

# Create Schema Registry client
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

# Create a Kafka consumer instance with Schema Registry integration
consumer_conf = {
    **kafka_conf,
    'key.deserializer': avro.AvroDeserializer(schema_registry_client),
    'value.deserializer': avro.AvroDeserializer(schema_registry_client)
}

consumer = Consumer(consumer_conf)

# Subscribe to a topic
consumer.subscribe(['my-avro-topic'])

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print(f"Reached end of partition {msg.partition()}")
            else:
                print(f"Error: {msg.error()}")
        else:
            # Process the received Avro-encoded message
            key = msg.key()
            value = msg.value()
            print(f"Received message - Key: {key}, Value: {value}")

except KeyboardInterrupt:
    pass

finally:
    consumer.close()
