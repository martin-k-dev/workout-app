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
    for item in list_to_clear:
        if item == "":
            list_to_clear.remove("")
    return list_to_clear
