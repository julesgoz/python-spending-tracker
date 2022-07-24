import csv
from unicodedata import category
import gspread
# MONTH = "JUNE"

file = r"C:\Users\Jules\Desktop\Python Projects\PythonFinances\python-spending-tracker\docs\Discover-Statement-20220720.csv"

with open(file, mode='r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        print(row)

sa = gspread.service_account()
sh = sa.open("Personal Finances")
