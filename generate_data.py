import os
import time
import io
import json
import logging
from faker import Faker
import uuid
import psycopg2

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

POSTGRES_USER = os.getenv("POSTGRES_USER", "user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
DATABASE_HOST = os.getenv("DATABASE_HOST", "127.0.0.1")
POSTGRES_DB = os.getenv("POSTGRES_DB", "eventlog")

ROWS_TO_GENERATE = int(os.getenv("ROWS_TO_GENERATE", "20000000"))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "10000"))

fake = Faker()


def generate_data():
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(
            host=DATABASE_HOST,
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
        )
        cursor = conn.cursor()
        total_rows = 0
        start_time = time.time()

        logger.info("Starting data generation for %s rows...", f"{ROWS_TO_GENERATE:,}")

        while total_rows < ROWS_TO_GENERATE:
            string_io = io.StringIO()

            for _ in range(BATCH_SIZE):
                event_name = fake.random_element(
                    elements=("page_view", "add_to_cart", "checkout", "user_signup")
                )
                user_id = uuid.uuid4()
                properties = json.dumps({
                    "url": fake.uri(),
                    "item_id": fake.random_int(min=1, max=100),
                })
                string_io.write(f"{event_name}\t{user_id}\t{properties}\n")

            string_io.seek(0)

            cursor.copy_expert(
                sql="COPY events (event_name, user_id, properties) FROM STDIN WITH (DELIMITER E'\\t')",
                file=string_io,
            )
            conn.commit()

            total_rows += BATCH_SIZE
            logger.info("Inserted %s / %s rows", f"{total_rows:,}", f"{ROWS_TO_GENERATE:,}")

        elapsed = time.time() - start_time
        logger.info("Finished inserting %s rows in %.2f seconds.", f"{total_rows:,}", elapsed)

    except psycopg2.Error:
        logger.exception("Database error during data generation")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    generate_data()
