#Revamped version of CS50P final project

# Import libraries
import csv
import requests
from datetime import date
import re
import pandas
from tabulate import tabulate 



from alpaca.data import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame



# Return stock info
def fetch(inpt, ans):

    url = f"https://data.alpaca.markets/v2/stocks/bars/latest?symbols={inpt}"

    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": "",
        "APCA-API-SECRET-KEY": ""
}

    response = requests.get(url, headers=headers)

    pos = ['open', 'close', 'low', 'high', 'all']
    if ans not in pos:
        raise ValueError

    try:

        if 'all' not in ans:
            z = response.json()['bars'][inpt][ans[0]]
            return f'\n~{ans}: ${z}\n'

        else:
            
            # Create list of prices
            x = response.json()['bars'][inpt]
            prices = list(x.values())

            # Writing info into a CSV
            with open('out.csv', 'w') as new_file:
                writer = csv.DictWriter(new_file, fieldnames=['Open', 'High', 'Low', 'Close'])
                writer.writeheader()
                writer.writerow({'Open': prices[4], 'High': prices[1], 'Low': prices[2], 'Close': prices[0]})
            
            # Printing to terminal in table format    
            with open('out.csv', 'r') as file:
                reader = csv.DictReader(file)
                table = tabulate(reader, headers="keys", tablefmt="grid")
            
            return table

    except KeyError:
        return "INVALID SYMBOL"

    except ValueError:
        return "INVALID POSITION"




# Return current price
def fetch_current(symbol):


    url = "https://data.alpaca.markets/v2/stocks/trades/latest?symbols=" + symbol

    headers = {
    "accept": "application/json",
            "APCA-API-KEY-ID": "",
        "APCA-API-SECRET-KEY": ""

}

    response = requests.get(url, headers=headers)


    try:

        # Return current price
        x = response.json()["trades"][symbol]["p"]
        return f'\n~current price of {symbol}: ${x}\n'


    except KeyError:
        return "INVAILD SYMBOL"



# Return crypto info
def fetch_crypto(symbol, ans):


    url = f"https://data.alpaca.markets/v1beta3/crypto/us/bars?symbols={symbol}&timeframe=1D&limit=1000&sort=asc"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)


    try:

        # Return current price
        if 'all' not in ans:
            z = response.json()['bars'][symbol][0][ans[0]]
            return f'\n~{ans}: ${z}\n'
        else:

            # Create list of prices
            x = response.json()['bars'][symbol][0]
            prices = list(x.values())
            
            # Writing info into a CSV
            with open('out_cr.csv', 'w') as new_file:
                writer = csv.DictWriter(new_file, fieldnames=['Open', 'High', 'Low', 'Close'])
                writer.writeheader()
                writer.writerow({'Open': prices[4], 'High': prices[1], 'Low': prices[2], 'Close': prices[0]})
            
            # Printing to terminal in table format    
            with open('out_cr.csv', 'r') as file:
                reader = csv.DictReader(file)
                table = tabulate(reader, headers="keys", tablefmt="grid")
                
                return table


    except KeyError:
        return "INVALID POSITION"



# Collect user input
def main():

    # Search for crypto format
    pattern = r'^[A-Z]+/[A-Z]+$'

    pos = ['open', 'high', 'low', 'close', 'all']
    while True:
        try:
            print("\n~For crypto please input in SYMBOL/CURRENCY format\n~to quit program press control+d\n")
            symbol = input("Enter ticker: ").strip()
            if symbol.islower() == True:
                print('INVALID SYMBOL')
                continue

            match = re.search(pattern, symbol)
            if match:

                c_ans = input("Specify open, close, high, low, current or all: ")
                print(fetch_crypto(symbol, c_ans))
                continue
            else:

                ans = input("Specify open, close, high, low, current or all: ").strip()

                if ans == 'current':
                    print(fetch_current(symbol))
                    continue
                elif ans in pos:
                    print(fetch(symbol, ans))
                    continue
                elif ans not in pos:
                    print("INVALID INPUT TRY AGAIN")
                    continue

        # User exits with ctrl + d            
        except EOFError:
            exit()



if __name__ == "__main__":
    main()
