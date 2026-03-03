CREATE TABLE IF NOT EXISTS workouts (
	id INTEGER PRIMARY KEY,
	date TEXT NOT NULL UNIQUE,
	name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS exercises (
	id INTEGER PRIMARY KEY,
	name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS workout_exercises (
	workout_id INTEGER NOT NULL,
	exercise_id INTEGER NOT NULL,
	series INTEGER,
	reps INTEGER,
	duration INTEGER,
	duration_type TEXT,
	weight REAL,
	weight_type TEXT,
	bonus_rep INTEGER,
	addition_info TEXT,

    PRIMARY KEY (workout_id, exercise_id),
	FOREIGN KEY(workout_id) REFERENCES workouts(id),
	FOREIGN KEY(exercise_id) REFERENCES exercises(id)

);

CREATE TABLE IF NOT EXISTS muscles (
	id INTEGER PRIMARY KEY,
	name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS exercise_muscles (
	exercise_id INTEGER,
	muscle_id INTEGER,
	PRIMARY KEY (exercise_id, muscle_id),
	FOREIGN KEY(exercise_id) REFERENCES exercises(id),
	FOREIGN KEY(muscle_id) REFERENCES muscles(id)
);
