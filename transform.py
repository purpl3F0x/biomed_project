from pathlib import Path
import csv
from shutil import copy2


BASE_DIR = Path.cwd()
IMAGES_DIR = BASE_DIR / "Osteosarcoma-UT"
EXPORT_DIR = BASE_DIR / "Dataset"

wild_files = 0
not_classified = 0
classes = {'Viable': 0, 'Non-Viable-Tumor': 0, 'Non-Tumor': 0}

files = []

for _class, _ in classes.items():
    (EXPORT_DIR/_class).mkdir(parents=True, exist_ok=True)

for training_set in IMAGES_DIR.iterdir():
    print(f"+ {training_set}")
    for _set in training_set.iterdir():
        print(f"\t-> {_set}")
        validation_file = _set / "PathologistValidation.csv"

        with open(validation_file, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                correct_file_name = row[0].replace(" - ", "-").replace(" ", "-")
                classification = row[1]
                if Path.exists(_set / correct_file_name):
                    if classification == "viable: non-viable":
                        not_classified += 1
                    else:
                        copy2(_set / correct_file_name,
                              EXPORT_DIR / classification)
                        if correct_file_name not in files:
                            files.append(correct_file_name)
                            classes[classification] += 1
                        else:
                            print(correct_file_name)

                else:
                    wild_files += 1

print()
print(classes, wild_files, not_classified)
