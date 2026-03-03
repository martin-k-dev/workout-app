import json
import datetime

def write_test_output(content: dict):
    # IF the file exists
    try:
        with open("test_output.json", "w", encoding="utf-8") as test_output_file:
            # data = {"Timestamp": datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"), "Content": content}
            data = content
            json.dump(data, test_output_file, indent=4, ensure_ascii=False)
            test_output_file.write("\n,")

    # If the file doesnt exist
    except FileNotFoundError:
        with open("test_output.json", "x", encoding="utf-8") as test_output_file:
            data = {"Timestamp": datetime.datetime.now().isoformat('YYYY-MM-DD HH:MM:SS'), "Content": content}
            json.dump(data, test_output_file, indent=4, ensure_ascii=False)
            test_output_file.write("\n,")