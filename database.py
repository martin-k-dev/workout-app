import sqlite3
from tkinter.constants import INSERT

from utilities import load_file
from parser import clear_data, read_example_files

DB_PATH = "workouts.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():
    connection = sqlite3.connect("workouts.db")
    cursor = connection.cursor()

    schema_sql = load_file("database/schema.sql")

    cursor.executescript(schema_sql)

    connection.commit()
    connection.close()


def populate_database(workouts_data: list[dict]):
    connection = get_connection()
    cursor = connection.cursor()

    for workout in workouts_data:
        insert_workout(cursor, workout)

    connection.commit()
    connection.close()


def insert_workout(cursor, workout: dict):
    """
    Available Keys for workout:
    'Date'
    'SessionName'
    'Exercises'
    """
    # Insert name and date into database
    cursor.execute("INSERT OR IGNORE INTO workouts (date, name) VALUES (?, ?)",
                   (workout["Date"], workout["SessionName"]))

    # Always fetch ID explicitly
    cursor.execute("SELECT id FROM workouts WHERE date = ? AND name = ?",
                   (workout["Date"], workout["SessionName"]))
    workout_id = cursor.fetchone()[0]

    for exercise in workout["Exercises"]:
        insert_exercise(cursor, exercise, workout_id)


def insert_exercise(cursor, exercise: dict, workout_id):
    """
    Available Keys for exercise:
    'ExerciseName'
    'SeriesAmount'
    'RepsAmount'
    'Duration'
    'DurationType'
    'Weight'
    'WeightType'
    'BonusRep'
    'MusclesWorked'
    'AdditionInfo'
    """
    # Try to insert an exercise into a table
    cursor.execute("INSERT OR IGNORE INTO exercises (name) VALUES (?)",
                   (exercise['ExerciseName'],))

    # Select an ID of the exercise
    cursor.execute("SELECT id FROM exercises WHERE name = ?",
                   (exercise['ExerciseName'],))
    exercise_id = cursor.fetchone()[0]

    cursor.execute("SELECT workout_id, exercise_id FROM workout_exercises WHERE workout_id = ? AND exercise_id = ?",
                   (workout_id, exercise_id))

    cursor.execute("INSERT OR IGNORE INTO workout_exercises (workout_id, exercise_id, series, reps, duration, "
                   "duration_type, weight, weight_type, bonus_rep, addition_info) "
                   "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (workout_id, exercise_id, exercise["SeriesAmount"], exercise["RepsAmount"],
                    exercise["Duration"], exercise["DurationType"], exercise["Weight"], exercise["WeightType"],
                    exercise["BonusRep"], exercise["AdditionInfo"]))

    # Insert worked muscles into database
    for muscle in exercise["MusclesWorked"]:
        insert_muscle_worked(cursor, muscle, exercise_id, workout_id)


def insert_muscle_worked(cursor, muscle, exercise_id, workout_id):
    # Try to insert a muscle into the table "muscles"
    cursor.execute("INSERT OR IGNORE INTO muscles (name) VALUES (?)",
                   (muscle,))

    cursor.execute("SELECT id FROM muscles WHERE name = ?",
                   (muscle,))

    muscle_id = cursor.fetchall()[0][0]

    cursor.execute("INSERT OR IGNORE INTO exercise_muscles (exercise_id, muscle_id) VALUES (?, ?)",
                   (exercise_id, muscle_id))


def drop_all_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        DROP TABLE IF EXISTS workout_exercises;
        DROP TABLE IF EXISTS exercises;
        DROP TABLE IF EXISTS workouts;
        DROP TABLE IF EXISTS exercise_muscles;
        DROP TABLE IF EXISTS muscles;
    """)

    conn.commit()
    conn.close()


def clear_all_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM workout_exercises;")
    cursor.execute("DELETE FROM exercises;")
    cursor.execute("DELETE FROM workouts;")
    cursor.execute("DELETE FROM exercise_muscles;")
    cursor.execute("DELETE FROM muscles;")
    cursor.execute("DELETE FROM sqlite_sequence;")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    initialize_database()
    populate_database(clear_data(read_example_files()))
    input("Clear tables?: ")
    clear_all_tables()
    input("Drop tables?: ")
    drop_all_tables()
