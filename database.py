import sqlite3
from utilities import load_file

def run_schema():
    connector = sqlite3.connect("workouts.db")
    cursor = connector.cursor()

    schema_sql = load_file("database/schema.sql")

    cursor.executescript(schema_sql)

    connector.commit()
    connector.close()


if __name__ == "__main__":
    run_schema()
