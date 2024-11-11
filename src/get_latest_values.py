import os
import time

import psycopg2
from dotenv import load_dotenv
from prettytable import PrettyTable

# Load environment variables from .env file
load_dotenv()


def get_latest_values(patient_id, metric, limit=5, interval=10):
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

    while True:
        with conn.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    SELECT patient_id, metric, value, timestamp
                    FROM patient_data
                    WHERE patient_id = %s AND metric = %s
                    ORDER BY timestamp DESC
                    LIMIT %s;
                    """,
                    (patient_id, metric, limit),
                )
                records = cursor.fetchall()

                if records:
                    # Create and display the table using PrettyTable
                    table = PrettyTable(["Patient ID", "Metric", "Value", "Timestamp"])
                    for record in records:
                        table.add_row(record)

                    # Clear the console and print the updated table
                    os.system("cls" if os.name == "nt" else "clear")
                    print("Latest Values:")
                    print(table)
                else:
                    print(f"No records found for patient_id={patient_id}, metric={metric}.")
            except psycopg2.Error as e:
                print(f"Database query error: {e}")

        # Wait for the specified interval before refreshing
        print(f"Updating in {interval} seconds...\n")
        time.sleep(interval)


# Example usage to retrieve the latest 5 pulse readings for 'patient1' every 10 seconds
if __name__ == "__main__":
    print("Starting periodic latest values retrieval.")
    get_latest_values("patient1", "pulse", limit=5, interval=2)
