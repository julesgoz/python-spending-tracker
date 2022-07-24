import csv
import gspread
import time


def discoverFin(file):
    transactions = {'january': [], 'february': [], 'march': [],
                    'april': [], 'may': [], 'june': [], 'july': [], 'august': [],
                    'september': [], 'october': [], 'november': [], 'december': []}
    months = {'01': 'january', '02': 'february', '03': 'march',
                    '04': 'april', '05': 'may', '06': 'june', '07': 'july', '08': 'august',
                    '09': 'september', '10': 'october', '11': 'november', '12': 'december'}

    with open(file, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if row[0] == 'Trans. Date':
                continue
            date = row[0]
            month = months[date[:2]]
            name = row[2]
            amount = float(row[3])
            category = row[4]
            if category == "Payments and Credits" or category == "Awards and Rebate Credits":
                continue
            transaction = (date, name, category, amount)
            transactions[month].append(transaction)
        return transactions


def main():
    # get csv data from bank generate file
    data = r"C:\Users\Jules\Desktop\Python Projects\PythonFinances\python-spending-tracker\docs\Discover-2022-YearToDateSummary.csv"

    # open connection to google spreadsheet
    sa = gspread.service_account()
    sh = sa.open("Personal Finances")

    # get transaction data organized
    transactions = discoverFin(data)
    for month in transactions.keys():
        wks = sh.worksheet(f"{month}")
        rows = transactions[month]
        # insert data into spreadsheet
        wks.insert_rows(rows, 7)
        time.sleep(2)


if __name__ == "__main__":
    main()
