import csv
from pathlib import Path

def load_file(name: str, array_fields: list[str] = ["texts", "annotated_texts"]):
    csv_path = Path(__file__).parent.parent / "data" / f"{name}.csv"
    with open(csv_path, "r", encoding="utf-8") as f:
        csv.field_size_limit(2 ** 20)  # Increase limit to 1MB (2^20 characters)
        all_instances = list(csv.DictReader(f))

    for instance in all_instances:
        if "puddle_id" in instance:
            instance["puddle_id"] = int(instance["puddle_id"])
        for field in array_fields:
            if field in instance:
                instance[field] = [t.strip() for t in instance[field].split("᛫")]
                instance[field] = [t for t in instance[field] if t != ""]

    return all_instances


def load_data(main_file: str, *modifiers: str):
    main_data = load_file(main_file)
    for modifier in modifiers:
        # Load modifier data
        modifier_data = load_file(modifier)
        dict_data = {(instance["puddle_id"], instance["example_id"]): instance for instance in modifier_data}

        # Update main data
        for instance in main_data:
            key = (instance["puddle_id"], instance["example_id"])
            if key in dict_data:
                instance.update(dict_data[key])

    return main_data

