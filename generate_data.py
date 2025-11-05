import time
import io
import json
from faker import Faker
import uuid
import psycopg2


# --Configuration--
CONN_STRING = "host='127.0.0.1' dbname='eventlog' user='user' password='password'"
ROWS_TO_GENERATE = 20_000_000 # 20M random data
BATCH_SIZE = 10_000 # 10,000 rows at a time

# -- setup --
fake = Faker()

# -- The Generation logic --
def generate_data():
    conn = psycopg2.connect(CONN_STRING)
    cursor = conn.cursor()
    total_rows = 0
    start_time = time.time()

    print(f"Starting data generation for {ROWS_TO_GENERATE} rows...")
    while total_rows < ROWS_TO_GENERATE:
        # create a virtual file in memory 
        string_io = io.StringIO()

        for _ in range(BATCH_SIZE):
            event_name = fake.random_element(elements=('page_view', 'add_to_cart', 'checkout', 'user_signup'))
            user_id = uuid.uuid4()
            properties = json.dumps({"url": fake.uri(), "item_id": fake.random_int(min=1, max=100)})

            # write a tab separated line to the virtual file
            string_io.write(f"{event_name}\t{user_id}\t{properties}\n")
        
        # Rewind the virtual file to the beginning 
        string_io.seek(0)

        # use copy_expert to stream the data to Postgres
        cursor.copy_expert(
            sql="COPY events (event_name, user_id, properties) FROM STDIN WITH (DELIMITER E'\\t')",
            file=string_io
        )
        conn.commit()

        total_rows += BATCH_SIZE
        print(f"Inserted {total_rows}/{ROWS_TO_GENERATE} rows...")

    cursor.close()
    conn.close()

    end_time = time.time()
    print(f"Finished inserting {total_rows} rows in {end_time - start_time:.2f} seconds.")


    
if __name__=="__main__":
    generate_data()