from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'market.prices',
    bootstrap_servers='localhost:9092',
    api_version=(0, 10, 1),
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    print(f"Received event: {message.value}")
