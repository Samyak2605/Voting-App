import json
import os
import time
import psycopg2
import redis

REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
DB_HOST = os.getenv('POSTGRES_HOST', 'db')
DB_NAME = os.getenv('POSTGRES_DB', 'votes')
DB_USER = os.getenv('POSTGRES_USER', 'postgres')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')


def ensure_schema(connection):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS results (
              vote_option TEXT PRIMARY KEY,
              vote_count INTEGER NOT NULL
            );
            """
        )
        connection.commit()


def main():
    r = redis.Redis(host=REDIS_HOST, db=0)

    while True:
        try:
            connection = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
            ensure_schema(connection)
            break
        except Exception:
            time.sleep(2)

    while True:
        item = r.blpop('votes', timeout=5)
        if not item:
            continue

        _, data = item
        try:
            payload = json.loads(data)
            vote = payload.get('vote')
            if not vote:
                continue

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO results (vote_option, vote_count)
                    VALUES (%s, 1)
                    ON CONFLICT (vote_option)
                    DO UPDATE SET vote_count = results.vote_count + 1;
                    """,
                    (vote,)
                )
                connection.commit()
        except Exception:
            connection.rollback()


if __name__ == '__main__':
    main()
