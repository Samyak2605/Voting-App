from flask import Flask, render_template
import os
import psycopg2

app = Flask(__name__)

DB_HOST = os.getenv('POSTGRES_HOST', 'db')
DB_NAME = os.getenv('POSTGRES_DB', 'votes')
DB_USER = os.getenv('POSTGRES_USER', 'postgres')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')


def get_counts():
    connection = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS results (
                  vote_option TEXT PRIMARY KEY,
                  vote_count INTEGER NOT NULL
                );
            """)
            connection.commit()
            cursor.execute("SELECT vote_option, vote_count FROM results ORDER BY vote_option ASC;")
            rows = cursor.fetchall()
            return {option: count for option, count in rows}
    finally:
        connection.close()


@app.route("/")
def index():
    counts = get_counts()
    return render_template("index.html", counts=counts)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
