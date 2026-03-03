import re
from test_output import write_test_output
from utilities import clean_whitespaces_front, clean_whitespaces_back, clear_list_of_empty_items
from datetime import datetime

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
OUTPUT FROM CLEAR_DATA() SHOULD LOOK SOMETHING LIKE THIS (FINAl TEMPLATE)
{ 
    "2025-11-22": {
        "SessionName": "name",
        "Exercises": [
            {
                "ExerciseName": "example name",
                "SeriesAmount": 3,
                "RepsAmount": 10,
                "Duration": null,
                "DurationType": null,
                "Weight": 35.0,
                "WeightType": "kg",
                "BonusRep": false,
                "MusclesWorked": [
                    "muscle 1",
                    "muscle 2"
                ],
                "AdditionInfo": "Weight is fine"
            },...
        ]
    },
    "2026-01-01": {
        "SessionName": "Example Session Name",
        "Exercises": [
            {
                "ExerciseName": "Plank",
                "SeriesAmount": 3,
                "RepsAmount": null,
                "Duration": 45,
                "DurationType": "s",
                "Weight": null,
                "WeightType": null,
                "BonusRep": false,
                "MusclesWorked": [],
                "AdditionInfo": null
            },...
        ]
    }   
}
"""


def read_example_files() -> list:
    with open("example_workout", "r", encoding="utf-8") as datafile:
        data = datafile.read()
        sessions: list = data.split("\n\n\n")
        return sessions


def clear_data(text: list[str]) -> dict:
    """
    Example of formatted data can be found at the top of this file (parser.py)
    :return: A formatted list of all workout sessions
    """
    sessions_list: list[str] = text
    sessions_dict: dict = {}
    date_pattern = re.compile("([0-9]+.[0-9]+.[0-9]*)([^\n]+)")

    # Goes through each whole session
    for session in sessions_list[1:]:
        exercises_list = []

        # Splits the section into separate lines
        session_cleared: list[str] = session.split("\n")

        # Cleans the list of empty ("") items
        session_cleared = clear_list_of_empty_items(session_cleared)

        # Assigns the session name and date to a variable and removes it from the list
        session_name_and_date = session_cleared[0]
        session_cleared.pop(0)

        session_date, session_name = re.findall(date_pattern, session_name_and_date)[0]
        session_name = clean_whitespaces_back(session_name)
        session_name = clean_whitespaces_front(session_name)

        formatted_date = convert_date_format(session_date)

        # Goes through each line separately
        for line in session_cleared:
            line_cleared = get_split_data(line)
            formatted_list = get_exercise_dicts(line_cleared[0], line_cleared[1], line_cleared[2])
            for i in formatted_list:
                exercises_list.append(i)

        # Writes one session info into the all sessions dict
        sessions_dict[formatted_date] = {"SessionName": session_name,
                                       "Exercises": exercises_list}

    return sessions_dict


def get_split_data(line: str) -> tuple[str, str, str | None]:
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
    numerical_values = clean_whitespaces_back(numerical_values)
    exercise_name = clean_whitespaces_back(exercise_name)
    exercise_name = clean_whitespaces_front(exercise_name)

    return exercise_name, numerical_values, muscles_worked


def get_exercise_dicts(exercise_name: str, numerical_values: str, muscles_worked: str) -> list:
    """
    Returns a specifically formatted dictionary with these keys:
    :param exercise_name:
    :param numerical_values:
    :param muscles_worked:
    :return:
    ExerciseName: str | None \n
    RepsAmount: int | None \n
    Duration: int | None \n
    DurationType: str | None \n
    Weight: float | None \n
    WeightType: str | None \n
    BonusRep: bool \n
    MusclesWorked: list | None \n
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
    # If there's only one type of repetition for an exercise, the loop will go through only once
    # If there's more types of repetition (different weight for example), this will create
    # a separate dictionary for each different type of repetition
    # Different repetition are marked by a comma
    diff_reps_uncleared = numerical_values.split(",")
    structured_data_multiple = []

    for specific_rep in diff_reps_uncleared:

        structured_data: dict = {"ExerciseName": exercise_name, "SeriesAmount": None, "RepsAmount": None,
                                 "Duration": None,
                                 "DurationType": None, "Weight": None, "WeightType": None, "BonusRep": False,
                                 "MusclesWorked": None, "AdditionInfo": None}

        if len(structured_data_multiple) == 0:
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
            else:
                structured_data["MusclesWorked"] = []
        else:
           structured_data["MusclesWorked"] = structured_data_multiple[0]["MusclesWorked"]

        # Bonus rep
        if "+" in numerical_values:
            structured_data["BonusRep"] = True

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
                structured_data["Duration"] = int(specific_rep_values[1][:-1])
            elif "s" in specific_rep_values[1]:
                structured_data["DurationType"] = "S"
                structured_data["Duration"] = int(specific_rep_values[1][:-1])
            else:
                structured_data["RepsAmount"] = int(specific_rep_values[1])

            # [2] is Weight+WeightType
            if "kg" in specific_rep_values[2]:
                structured_data["WeightType"] = "KG"
                structured_data["Weight"] = float(specific_rep_values[2][:-2])

        # [0-9]x[0-9]kg   [0-9]x[0-9]s   [0-9]x[0-9]m
        else:
            specific_rep_split = specific_rep.split("x")
            structured_data["SeriesAmount"] = int(specific_rep_split[0])
            if "kg" in specific_rep_split[1]:
                structured_data["Weight"] = float(specific_rep_split[1][:-2])
                structured_data["WeightType"] = specific_rep_split[1][-2:]
                structured_data["RepsAmount"] = 10
            if "s" in specific_rep_split[1]:
                structured_data["Duration"] = int(specific_rep_split[1][:-1])
                structured_data["DurationType"] = specific_rep_split[1][-1:]

        structured_data_multiple.append(structured_data)

    return structured_data_multiple


def convert_date_format(date) -> str:
    """
    Converts a date from the file format to database storable format
    :param date: date to convert
    :return:a properly formatted date
    """
    # Converting date to a format suitable for database storage
    session_date_split = date.split(".")
    clear_list_of_empty_items(session_date_split)

    # If year is missing in entry, assign 2025
    if len(session_date_split) < 3:
        day, month = session_date_split[0], session_date_split[1]
        year = "2025"
    else:
        day, month, year = session_date_split[0], session_date_split[1], "20" + session_date_split[2]

    formatted_date = datetime(int(year), int(month), int(day)).strftime("%Y-%m-%d")
    return formatted_date


if __name__ == "__main__":
    write_test_output(clear_data())
