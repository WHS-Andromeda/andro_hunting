import os


def listToText(items, output_fn, output_dir):
    if not isinstance(items, list):
        raise ValueError("The 'items' parameter must be a list.")
    output_path = os.path.join(output_dir, output_fn)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as file:
        file.writelines(f"{item}\n" for item in items)


def readText(input_fn, input_dir="./"):
    input_path = os.path.join(input_dir, input_fn)
    with open(input_path, "r") as file:
        text_list = [line.strip() for line in file]
    return text_list
