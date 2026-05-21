import psycopg2
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'market.prices',
    bootstrap_servers='localhost:9092',
    api_version=(0, 10, 1),
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

conn = psycopg2.connect(
    host="localhost",
    port=5000,
    database="db_bpa",
    user="db_user",
    password="db_password"
)

cursor = conn.cursor()

for message in consumer:
    event = message.value

    cursor.execute(
        """
        INSERT INTO crypto_data_tb (
            symbol,
            price,
            market_cap,
            volume_24h,
            change_24h,
            currency,
            event_timestamp
        )
        VALUES (%s, %s, %s, %s, %s, %s, TO_TIMESTAMP(%s))
        """,
        (
            event["symbol"],
            event["price"],
            event["market_cap"],
            event["volume_24h"],
            event["change_24h"],
            event["currency"],
            event["timestamp"]
        )
    )

    conn.commit()

    print(f"Inserted event: {event}")