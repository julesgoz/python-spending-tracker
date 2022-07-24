import csv

# MONTH = "JUNE"

file = "python-spending-tracker\docs\Discover-Statement-20220720.csv"

with open(file, mode='r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        print(row)
