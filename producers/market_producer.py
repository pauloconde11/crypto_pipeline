from kafka import KafkaProducer
from services.api_clients.coingecko import fetch_market_data
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    api_version=(0, 10, 1),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def publish_market_data():

    market_data = fetch_market_data()

    for event in market_data:
        future = producer.send('market.prices', value=event)
        metadata = future.get(timeout=10)

        print(f"Sent event: {event}")
        print(metadata)

    producer.flush()
    producer.close()

def main():
    publish_market_data()
    
    
if __name__ == "__main__":
    main()

#python3 -m producers.market_producer


