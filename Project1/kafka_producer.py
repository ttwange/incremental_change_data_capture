from confluent_kafka import Producer
import json
import random
from datetime import datetime, timedelta
import psycopg2

# Kafka producer configuration
conf = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'coin-data-producer'
}

producer = Producer(conf)
# PostgreSQL database configuration
db_conn = psycopg2.connect(
    host='postgres',
    port='5432',
    dbname='exampledb',
    user='docker',
    password='docker'
)
db_cursor = db_conn.cursor()

# Generate and publish sample data to Kafka and insert into PostgreSQL
for _ in range(10):  # You can adjust the number of records as needed
    claim_id = random.randint(1, 1000)
    claim_date = datetime.today() - timedelta(days=random.randint(1, 365))
    member_id = random.randint(1, 100)
    claim_status = random.choice(['A', 'P', 'D'])

    drug_id = random.randint(1, 100)
    drug_name = f"Drug{drug_id}"
    drug_price = round(random.uniform(10, 100), 3)

    member_id = random.randint(1, 100)
    member_name = f"Member{member_id}"
    member_dob = datetime.today() - timedelta(days=random.randint(365 * 18, 365 * 60))

    # Publish to Kafka
    kafka_data = {
        "claim_id": claim_id,
        "claim_date": claim_date.strftime('%Y-%m-%d'),
        "member_id": member_id,
        "claim_status": claim_status,
        "drug_id": drug_id,
        "drug_name": drug_name,
        "drug_price": drug_price,
        "member_name": member_name,
        "member_dob": member_dob.strftime('%Y-%m-%d')
    }

    producer.send('postgres.public.claims', json.dumps(kafka_data).encode('utf-8'))

    # Insert into PostgreSQL
    db_cursor.execute("INSERT INTO public.claims VALUES (%s, %s, %s, %s)", (claim_id, claim_date, member_id, claim_status))
    db_cursor.execute("INSERT INTO public.drugs VALUES (%s, %s, %s)", (drug_id, drug_name, drug_price))
    db_cursor.execute("INSERT INTO public.member VALUES (%s, %s, %s)", (member_id, member_name, member_dob))

    db_conn.commit()

db_cursor.close()
db_conn.close()
