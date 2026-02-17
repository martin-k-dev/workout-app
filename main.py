import re
from test_output import write_test_output
from utilities import clean_whitespaces_front, clean_whitespaces_back, clear_list_of_empty_items

# WORKOUT APP

# will track separate sessions of workout

# tracks:
# date,
# exercise name,
# number of sets,
# number of reps within sets,
# number of weight,
# muscles worked
# Kg or seconds, minutes
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
        session_cleared = clear_list_of_empty_items(session_cleared)

        # Assigns the session name to a variable and removes it from the list
        session_name = session_cleared[0]
        session_cleared.pop(0)

        # Goes through each line separately
        for line in session_cleared:
            line_cleared = get_exact_data(line)
            get_formatted_list(line_cleared[0], line_cleared[1], line_cleared[2])


def get_exact_data(line: str) -> tuple[str, str, str | None]:
    """
    :param line: a line to split into
    :return:
    exercise_name: str
    numerical_value: str
    muscles_worked: str, None
    """
    exercise_name = None
    numerical_values = None
    muscles_worked = None

    # if there is a reference of muscles, returns whatever it found
    if '[' in line:
        pattern = re.compile("([^0-9]+)([^\\[]+)([^\n]+)")
        exercise_name, numerical_values, muscles_worked = re.findall(pattern, line)[0]

    # No reference of muscles worked, returns none for the third parameter
    else:
        pattern = re.compile("([^0-9]+)([^\n]+)")
        exercise_name, numerical_values = re.findall(pattern, line)[0]

    # Clears the numerical_values of any whitespaces that are at the end of the string
    clean_whitespaces_back(numerical_values)

    return exercise_name, numerical_values, muscles_worked


def get_formatted_list(exercise_name: str, numerical_values: str, muscles_worked: str) -> dict:
    """
    Returns a specifically formatted dictionary with these keys:
    :param exercise_name:
    :param numerical_values:
    :param muscles_worked:
    :return:
    ExerciseName: str | None \n
    RepsAmount: str | None \n
    Duration: str | None \n
    DurationType: str | None \n
    Weight: str | None \n
    WeightType: str | None \n
    BonusRep: str | None \n
    MusclesWorked: str | None \n
    AdditionInfo: str | None
    """
    """
    DEV NOTES
    POSSIBLE KNOWN SCENARIOS:
    [0-9]x[0-9]kg DONE
    [0-9]x[0-9]s DONE
    [0-9]x[0-9]m DONE
    [0-9]x[0-9] [0-9]kg DONE
    [0-9]x[0-9]s/m [0-9]kg DONE
    """
    structured_data: dict = {"ExerciseName": exercise_name, "SeriesAmount": None, "RepsAmount": None, "Duration": None,
                             "DurationType": None, "Weight": None,"WeightType": None, "BonusRep": False,
                             "MusclesWorked": None, "AdditionInfo": None}

    # Clear up the muscle_worked parameter
    if muscles_worked is not None:
        if '[' in muscles_worked:
            muscles_worked = muscles_worked[1:]
        if ']' in muscles_worked:
            muscles_worked = muscles_worked[:-1]
        muscles_worked_list = muscles_worked.split(',')

        # Removes whitespaces from both the beginning and the end of the content of the muscles_worked_list
        for index in range(len(muscles_worked_list)):
            muscles_worked_list[index] = clean_whitespaces_front(muscles_worked_list[index])
            muscles_worked_list[index] = clean_whitespaces_back(muscles_worked_list[index])

        structured_data["MusclesWorked"] = muscles_worked_list

    # If there's only one type of repetition for an exercise, the loop will go through only once
    # If there's more types of repetition (different weight for example), this will create
    # a separate dictionary for each different type of repetition
    # Different repetition are marked by a comma
    diff_reps_uncleared = numerical_values.split(",")
    for specific_rep in diff_reps_uncleared:

        # Removes whitespaces from both the beginning and the end of the string
        specific_rep = clean_whitespaces_back(specific_rep)
        specific_rep = clean_whitespaces_front(specific_rep)

        # [0-9]x[0-9] [0-9]kg / [0-9]x[0-9]s/m [0-9]kg
        if " " in specific_rep:

            # Splits the string into different values
            specific_rep_split = specific_rep.split(" ")
            specific_rep_values = specific_rep_split[0].split("x") + [specific_rep_split[1]]

            # Checks for additional info (basically something that doesn't fit in any category)
            if len(specific_rep_split) >= 3:
                additionalData = ""
                for i in range(1, len(specific_rep_split)):
                    additionalData = additionalData + " " + specific_rep_split[i]
                structured_data["AdditionInfo"] = additionalData

            # [0] is SeriesAmount
            structured_data["SeriesAmount"] = specific_rep_values[0]

            # [1] is RepsAmount/Duration+DurationType
            if "m" in specific_rep_values[1]:
                structured_data["DurationType"] = "M"
                structured_data["Duration"] = specific_rep_values[1][:-1]
            elif "s" in specific_rep_values[1]:
                structured_data["DurationType"] = "S"
                structured_data["Duration"] = specific_rep_values[1][:-1]
            else:
                structured_data["RepsAmount"] = specific_rep_values[1]

            # [2] is Weight+WeightType
            if "kg" in specific_rep_values[2]:
                structured_data["WeightType"] = "KG"
                structured_data["Weight"] = specific_rep_values[2][:-2]

        else:
            specific_rep_split = specific_rep.split("x")
            structured_data["SeriesAmount"] = specific_rep_split[0]
            if "kg" in specific_rep_split[1]:
                structured_data["Weight"] = specific_rep_split[1][:-2]
                structured_data["WeightType"] = specific_rep_split[1][-2:]
                structured_data["RepsAmount"] = "10"
            if "s" in specific_rep_split[1]:
                structured_data["Duration"] = specific_rep_split[1][:-1]
                structured_data["DurationType"] = specific_rep_split[1][-1:]

    write_test_output(structured_data)
    return structured_data

if __name__ == "__main__":
    print(clear_data())
