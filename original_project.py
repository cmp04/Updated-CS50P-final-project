# This is a program that will fetch the High, Low, Open, Close & Current price a given stock & or crypto currency
import requests
from datetime import date
import re
import pandas


from alpaca.data import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame


#return stock info

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
            x = response.json()['bars'][inpt]
            prices = list(x.values())
            c = f'\n~close ${prices[0]}, high: ${prices[1]}, low: ${prices[2]}, open: ${prices[4]}\n'
            return c

    except KeyError:
        return "INVALID SYMBOL"

    except ValueError:
        return "INVALID POSITION"




#return current price

def fetch_current(symbol):


    url = "https://data.alpaca.markets/v2/stocks/trades/latest?symbols=" + symbol

    headers = {
    "accept": "application/json",
            "APCA-API-KEY-ID": "",
        "APCA-API-SECRET-KEY": ""

}

    response = requests.get(url, headers=headers)

    try:
        x = response.json()["trades"][symbol]["p"]
        return f'\n~current price of {symbol}: ${x}\n'

    except KeyError:
        return "INVAILD SYMBOL"



#return crypto info

def fetch_crypto(symbol, ans):

    url = f"https://data.alpaca.markets/v1beta3/crypto/us/bars?symbols={symbol}&timeframe=1D&limit=1000&sort=asc"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)


    try:
        if 'all' not in ans:
            z = response.json()['bars'][symbol][0][ans[0]]
            return f'\n~{ans}: ${z}\n'
        else:
            x = response.json()['bars'][symbol][0]
            prices = list(x.values())
            c = f'\n~current: ${prices[0]}, high: ${prices[1]}, low: ${prices[2]}, open: ${prices[4]}\n'
            return c

    except KeyError:
        return "INVALID POSITION"



#collect user input

def main():
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
        except EOFError:
            exit()



if __name__ == "__main__":
    main()
