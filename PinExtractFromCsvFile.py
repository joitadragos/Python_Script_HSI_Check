import csv

#We'll use this script to extract the pin names and their functions from the CSV file exported from the Excel sheet, so that we can compare them with the pin configuration in the code.

# Export the sheet "HSI" from
# "HSI.xls" as a CSV file first,
# then set INPUT_CSV to that file's name.
INPUT_CSV   = "HSI.csv"   #here to use the Hw_Sw_Intf path for the .csv file
START_ROW   = 9          # 1-based; data begins on this row
COL_B       = 1          # column A  (0-based)
COL_AS      = 44         # column AS (0-based, A=0 … AS=44)
OUTPUT_CSV  = "Results.csv"

# ---------- read ---------------------------------------------------------
rows = []
with open(INPUT_CSV, newline="", encoding="cp1252") as f:
    reader = csv.reader(f)
    for row_num, row in enumerate(reader, start=1):
        if row_num < START_ROW:
            continue
        val_a  = row[COL_B]  if len(row) > COL_B  else ""
        val_as = row[COL_AS] if len(row) > COL_AS else ""
        rows.append((val_a, val_as))

# ---------- write --------------------------------------------------------
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["Column A", "Column AS"])
    writer.writerows(rows)

print("Done. {} rows written to {}".format(len(rows), OUTPUT_CSV))
