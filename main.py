import re


# WORKOUT APP

# will track separate sessions of workout

# tracks:
# date,
# exercise name,
# number of sets,
# number of reps within sets,
# number of weight,
# muscles worked
# Kg or seconds
# If bonus rep was done

"""
OUTPUT SHOULD LOOK SOMETHING LIKE THIS (FIRST TEMPLATE)
session_dict{ 
    session_name1: {
        exercise_name1: {
            numerical_values1: xx
            muscles_worked1: xx
            value_type1: xx
        },
        exercise_name2: {
            numerical_values2: xx
            muscles_worked2: xx
            value_type2: xx
        }...
    },
    session_name2: {
        exercise_name1: {
            numerical_values1: xx
            muscles_worked1: xx
            value_type1: xx
        },
        exercise_name2: {
            numerical_values2: xx
            muscles_worked2: xx
            value_type2: xx
        }
    }...
}
"""


def read_files() -> list:
    with open("example_workout", "r", encoding="utf-8") as datafile:
        data = datafile.read()
        sessions: list = data.split("\n\n\n")
        return sessions

def clear_data():
    sessions_list: list[str] = read_files()
    exercises_list = []
    sessions_dict: dict = {}


    # Goes through each whole session
    for session in sessions_list[1:]:
        # Splits the section into separate lines
        session_cleared: list[str] = session.split("\n")

        # Cleans the list of empty ("") items
        for i in session_cleared:
            if i == "":
                session_cleared.remove("")

        # Assigns the session name to a variable and removes it from the list
        session_name = session_cleared[0]
        session_cleared.pop(0)

        # Goes through each line separately
        for line in session_cleared:
            print(get_exact_data(line))

def get_exact_data(line: str):
    """

    :param line: a line to split into
    :return:
    exercise_name: str
    numerical_value: str
    """
    exercise_name = None
    numerical_values = None
    muscles_worked = None
    if '[' in line:
        pattern = re.compile("([^0-9]+)([^\\[]+)([^\n]+)")
        exercise_name, numerical_values, muscles_worked = re.findall(pattern, line)[0]
    else:
        # No reference of muscles worked, returns none for the third parameter
        pattern = re.compile("([^0-9]+)([^\n]+)")
        exercise_name, numerical_values = re.findall(pattern, line)[0]
    return exercise_name, numerical_values, muscles_worked


if __name__ == "__main__":
    print(clear_data())
