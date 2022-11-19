from tkinter import filedialog
import os
import requests
import json


def retrieve_file_paths(f_type='.pdf') -> list[str]:
    """Given directory all PDFs within that directory and organizes their file paths into a list"""
    t = f"Select directory with given {f_type} files"
    f_paths = []

    # request directory with PDF files (not exclusive to OS system) use tkinter for a directory (using a gui selector)
    dir_name = filedialog.askdirectory(initialdir="/", title=t)
    for file in os.listdir(dir_name):
        # check if file exists and if file is also a pdf extension
        if os.path.isfile(os.path.join(dir_name, file)) and os.path.splitext(file.title())[1].lower() == f_type:
            f_paths.append(os.path.join(dir_name, file))

    # return list of paths
    return f_paths


def make_requests(file_paths):
    """Given a list of file paths we create multiple instances of post requests throughout the entire folder"""
    output = {}
    app_id, app_key = json.load(open('api_key.json', 'rb'))['APP_ID'], json.load(open('api_key.json', 'rb'))['API_KEY']
    ct = 1
    for p in file_paths:
        _f = open(p, 'rb')
        print(p, _f)

        _request = requests.post(
            "https://api.mathpix.com/v3/text",
            files={"file": _f},
            data={
                "options_json": json.dumps({
                    "math_inline_delimiters": ["$", "$"],
                    "rm_spaces": True
                })
            },
            headers={
                "app_id": app_id,
                "app_key": app_key
            }
        )

        print(_request.json())

        # output[p] = json.dumps(, indent=4, sort_keys=True)
        output[p] = _request.json()
        print(type(_request.json()))
        ct += 1

    return output


if __name__ == '__main__':
    try:
        # Active path for the directory, will throw an IndexError if no previous files have been created
        path = os.path.join(os.getcwd(), f'JSON_OUTPUTS/{os.listdir(os.path.join(os.getcwd(), "JSON_OUTPUTS"))[-1]}')
        f = open(path, 'w')
    except IndexError:
        # Catch for the IndexError and creates a new file
        f = open(os.path.join(os.getcwd(), 'JSON_OUTPUTS/output.json'), 'w')

    # Make and write serialized json requests to the json file
    f_paths = retrieve_file_paths('.jpeg')
    r = make_requests(f_paths)

    print(r)
    f.write(json.dumps(r, indent=4, sort_keys=True))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
