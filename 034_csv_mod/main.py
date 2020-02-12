# 034. csv
#
# reader, DictReader, writer, and dialects.
#
# Run: python 034_csv_mod/main.py

# --- csv mod ---
import csv

from io import StringIO

buf = StringIO("name,year\nAda,1815\nAlan,1912\n")
print(list(csv.reader(buf)))
out = StringIO()
w = csv.writer(out)
w.writerow(["name", "year"])
w.writerow(["Ada", 1815])
print(out.getvalue())

# --- csv dict ---
import csv

from io import StringIO

text = "name,year\nAda,1815\n"
rows = list(csv.DictReader(StringIO(text)))
print(rows[0]["name"], rows[0]["year"])

# --- csv writer ---
import csv

from io import StringIO

buf = StringIO()
w = csv.writer(buf, delimiter=";", lineterminator="\n")
w.writerow(["a", "b;c"])
print(buf.getvalue())
