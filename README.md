# Working with Real-Time Data? TimescaleDB Might Be the Simple, Scalable Solution You Need

This repository contains the code for the blog post [Working with Real-Time Data? TimescaleDB Might Be the Simple, Scalable Solution You Need](https://arrangeactassert.com/posts/real-time-timescaledb/).

![Real-Time TimescaleDB](real-time-timescaledb.gif)

## Running the code

1. **Clone this repository**:

   ```bash
   git clone https://github.com/jagreehal/real-time-timescaledb
   cd real-time-timescaledb
   ```

2. **Set up the virtual environment and install dependencies using uv**:

   ```bash
   make install
   ```

   This command uses uv to create and manage the virtual environment and install dependencies.

3. **Activate the virtual environment**:

- On Unix or MacOS:

  ```bash
  source .venv/bin/activate
  ```

- On Windows:

- ```bash
  .venv\Scripts\activate
  ```

## Start the TimescaleDB container

```bash
make docker-compose up -d
```

## Create the database, table, and materialized view

```bash
CREATE TABLE IF NOT EXISTS patient_data (
    patient_id TEXT NOT NULL,
    metric TEXT NOT NULL,
    value DOUBLE PRECISION,
    timestamp TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (patient_id, metric, timestamp)
);

SELECT create_hypertable('patient_data', 'timestamp', if_not_exists => TRUE);

CREATE MATERIALIZED VIEW IF NOT EXISTS latest_pulse AS
SELECT DISTINCT ON (patient_id)
    patient_id,
    metric,
    timestamp AS latest_timestamp,
    value AS latest_value
FROM patient_data
WHERE metric = 'pulse'
ORDER BY patient_id, timestamp DESC;
```

## Start the data ingestion script

```bash
python src/data_ingestion.py
```

## Start the data visualization script

In another terminal, run the following command:

```bash
python src/get_latest_values.py
```

## License

This project is licensed under the MIT License
