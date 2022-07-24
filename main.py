import csv
import gspread
import time

MONTH = "june"
file = r"C:\Users\Jules\Desktop\Python Projects\PythonFinances\python-spending-tracker\docs\Discover-Statement-20220720.csv"


def discoverFin(file):
    transactions = []
    with open(file, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            date = row[0]
            name = row[2]
            amount = row[3]
            category = row[4]
            if category == "Payments and Credits":
                continue
            transaction = (date, name, amount, category)
            transactions.append(transaction)
        return transactions


sa = gspread.service_account()
sh = sa.open("Personal Finances")

wks = sh.worksheet(f"{MONTH}")

rows = discoverFin(file)[1:]

for row in rows:
    wks.insert_row([row[0], row[1], row[3], row[2]], 8)
    time.sleep(2)
