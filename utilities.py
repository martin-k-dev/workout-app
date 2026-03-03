def clean_whitespaces_front(string_to_clean: str) -> str:
    for i in range(len(string_to_clean)):
        if string_to_clean.startswith(" "):
            string_to_clean = string_to_clean[1:]
        else:
            break
    return string_to_clean


def clean_whitespaces_back(string_to_clean: str) -> str:
    for i in range(len(string_to_clean)):
        if string_to_clean.endswith(" "):
            string_to_clean = string_to_clean[:-1]
        else:
            break
    return string_to_clean


def clear_list_of_empty_items(list_to_clear: list):
    """
    Cleans a list of ""
    :param list_to_clear:
    :return: A cleared list
    """
    for item in list_to_clear:
        if item == "":
            list_to_clear.remove("")
    return list_to_clear


def try_convert_to_type(item, type_to_convert_to, value_if_fail):
    """
    Available types - "int", "float", "bool", "str"
    :param item: item to convert
    :param type_to_convert_to: type to convert to
    :param value_if_fail: value returned if type conversion returns an empty string
    :return:
    """
    types = ["int", "float", "bool", "str"]
    if type_to_convert_to in types:
        try:
            match type_to_convert_to:
                case "int":
                    return int(item)
                case "float":
                    return float(item)
                case "bool":
                    return bool(item)
                case "str":
                    return str(item)
        except ValueError:
            return value_if_fail
    else:
        raise ValueError("Type of conversion not found")


def load_file(filepath):
    """
    Reads a file and returns it's whole content
    :param filepath:
    :return:
    """
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()
