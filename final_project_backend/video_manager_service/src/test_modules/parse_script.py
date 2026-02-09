import csv

input_file = 'debug_output_2025-04-28_09-42-18.csv'
output_file = 'parsed_output.csv'

# ניצור מבנה נתונים שבו נרכז את כל שמות חלקי הגוף
all_body_parts = set()

# שלב 1: מעבר על הקובץ כדי לאסוף את כל שמות איברי הגוף
with open(input_file, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        parts_str = row['body_parts_distances']
        if parts_str:
            parts = parts_str.strip().split()
            for p in parts:
                name, _ = p.split(':')
                all_body_parts.add(name)

# נמיין את האיברים לפי סדר א-ב
sorted_body_parts = sorted(all_body_parts)

# שלב 2: יצירת הקובץ החדש
with open(input_file, newline='') as csvfile, open(output_file, 'w', newline='') as outfile:
    reader = csv.DictReader(csvfile)

    # נגדיר את עמודות הפלט
    fieldnames = ['frame_number', 'timestamp']
    for part in sorted_body_parts:
        fieldnames.append(f'{part}_adult')
        fieldnames.append(f'{part}_child')
    fieldnames += ['threshold', 'num_detected_body_parts']

    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        output_row = {
            'frame_number': row['frame_number'],
            'timestamp': row['timestamp'],
            'threshold': row['threshold'],
            'num_detected_body_parts': row['num_detected_body_parts']
        }

        # ננקה את הערכים עבור כל עמודה מראש
        for part in sorted_body_parts:
            output_row[f'{part}_adult'] = ''
            output_row[f'{part}_child'] = ''

        parts_str = row['body_parts_distances']
        if parts_str:
            parts = parts_str.strip().split()
            for p in parts:
                try:
                    name, values = p.split(':')
                    adult_val, child_val = values.split(',')
                    output_row[f'{name}_adult'] = adult_val
                    output_row[f'{name}_child'] = child_val
                except ValueError:
                    # טיפול במקרה חריג – לדוגמה מחרוזת לא תקנית
                    continue

        writer.writerow(output_row)
   