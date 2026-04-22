import os
import csv

# Get project root (VERY IMPORTANT)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Correct paths
images_dir = os.path.join(BASE_DIR, "data", "images")
labels_dir = os.path.join(BASE_DIR, "data", "labels")
csv_path = os.path.join(BASE_DIR, "data", "CSVs", "dataset.csv")

# Get all filenames
image_files = sorted(os.listdir(images_dir))

with open(csv_path, "w", newline="") as f:
    writer = csv.writer(f)

    writer.writerow(["image_path", "label_path"])

    for img in image_files:
        if not img.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        # RELATIVE paths (IMPORTANT FOR PORTABILITY)
        image_rel = os.path.join("data", "images", img)
        label_name = os.path.splitext(img)[0] + ".txt"
        label_rel = os.path.join("data", "labels", label_name)

        writer.writerow([image_rel, label_rel])

print("dataset.csv created successfully")