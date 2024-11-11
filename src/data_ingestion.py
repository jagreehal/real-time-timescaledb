import os
import random
import time
from datetime import datetime

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import execute_batch

# Load environment variables from .env file
load_dotenv()


def ingest_data_batch(batch_size=10, interval=5):
    # Retrieve the database URL from the .env file
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("Error: DATABASE_URL is not set in the environment.")
        raise ValueError("DATABASE_URL is not set in the environment.")

    # Establish connection using the database URL
    try:
        conn = psycopg2.connect(database_url)
        print("Connected to the database successfully.")
    except psycopg2.OperationalError as e:
        print(f"Database connection error: {e}")
        return

    with conn.cursor() as cursor:
        patients = ["patient1", "patient2", "patient3"]
        metrics = ["pulse", "temperature"]

        while True:
            data_batch = []
            for _ in range(batch_size):
                patient = random.choice(patients)
                metric = random.choice(metrics)
                value = random.uniform(60, 100) if metric == "pulse" else random.uniform(36, 38)
                timestamp = datetime.utcnow()
                data_batch.append((patient, metric, value, timestamp))

            # Execute batch insert
            try:
                execute_batch(
                    cursor,
                    """
                    INSERT INTO patient_data (patient_id, metric, value, timestamp)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (patient_id, metric, timestamp) DO NOTHING;
                    """,
                    data_batch,
                )
                conn.commit()
                print(f"Batch of {batch_size} records upserted successfully.")
            except psycopg2.Error as e:
                print(f"Database error during batch insert: {e}")
                conn.rollback()

            # Wait before the next batch insert
            print(f"Next update in {interval} seconds...\n")
            time.sleep(interval)


if __name__ == "__main__":
    print("Starting batch data ingestion process.")
    ingest_data_batch(batch_size=10, interval=1)
