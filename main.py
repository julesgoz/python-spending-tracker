import csv
import gspread
import time


def discoverFin(file, transactions):
    with open(file, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if row[0] == 'Trans. Date':
                continue
            date = row[0]
            month = months[date[:2]]
            name = row[2]
            amount = -float(row[3])
            category = row[4]
            transaction = (date, name, category, amount)
            transactions[month].append(transaction)
        return transactions


def findCategory(name):
    categories = {'Montrose': '*RENT & BILLS*', 'VENMO': '*RENT & BILLS*', 'COINBASE': 'Crypto', 'AMZN': 'Merchandise', 'Amazon': 'Merchandise', 'DUKEENERGY': '*RENT & BILLS*',
                  'DISCOVER': 'IGNORE'}
    for i in range(1, len(name)):
        if name[0:i] in categories:
            return categories[name[0:i]]
    return 'other'


def chaseFin(file, transactions):
    with open(file, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if row[0] == 'Details':
                continue
            date = row[1]
            month = months[date[:2]]
            name = row[2]
            amount = float(row[3])
            category = findCategory(name)
            if category == "Payments and Credits" or category == "Awards and Rebate Credits" or category == "IGNORE":
                continue
            transaction = (date, name, category, amount)
            transactions[month].append(transaction)
        return transactions


def main():
    # get csv data from bank generate file
    discoverData = r"C:\Users\Jules\Desktop\Python Projects\PythonFinances\python-spending-tracker\docs\Discover-2022-YearToDateSummary.csv"
    chaseData = r"C:\Users\Jules\Desktop\Python Projects\PythonFinances\python-spending-tracker\docs\Chase7438_Activity_20220724.CSV"

    # open connection to google spreadsheet
    sa = gspread.service_account()
    sh = sa.open("Personal Finances")

    # get transaction data organized
    global months
    months = {'01': 'january', '02': 'february', '03': 'march',
                    '04': 'april', '05': 'may', '06': 'june', '07': 'july', '08': 'august',
                    '09': 'september', '10': 'october', '11': 'november', '12': 'december'}

    transactions = {'january': [], 'february': [], 'march': [],
                    'april': [], 'may': [], 'june': [], 'july': [], 'august': [],
                    'september': [], 'october': [], 'november': [], 'december': []}
    transactions = discoverFin(discoverData, transactions)
    transactions = chaseFin(chaseData, transactions)

    for month in transactions.keys():
        wks = sh.worksheet(f"{month}")
        wks.delete_rows(7, 150)
        rows = transactions[month]
        rows = sorted(rows, key=lambda row: row[0])
        # insert data into spreadsheet
        wks.insert_rows(rows, 7)
        time.sleep(2)


if __name__ == "__main__":
    main()
