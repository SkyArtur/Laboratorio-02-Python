from pathlib import Path
import json


def reader(filename):
    try:
        root = Path(__file__).resolve().parent.parent.joinpath('files')
        with open(root.joinpath(filename), encoding="utf-8") as file:
            if '.json' in filename:
                return json.load(file)
            else:
                return file.read()
    except (FileNotFoundError, TypeError) as error:
        return f'Error reading {filename}: {error}'


