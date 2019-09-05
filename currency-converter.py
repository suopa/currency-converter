import argparse
import sys
import json
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

def main():
    parser = argparse.ArgumentParser(description="Command line currency converter")
    parser.add_argument('--base', type=str, default="EUR", help='Convert from currency. Default: EUR')
    parser.add_argument('--target', type=str, default="USD", help='Convert to currency. Default: USD')
    parser.add_argument('--amount', type=float, default=1.0, help='Amount of the base currency to convert. Default: 1.0')
    args = parser.parse_args()
    
    if isValidCurrency(args.base) and isValidCurrency(args.target):
        content = getApiContentAsJson(args)
        rate = getExchangeRate(content, args)

        targetAmount = round(args.amount * rate, 4)

        print(str(args.amount) + " " + args.base + " == " + str(targetAmount) + " " + args.target)
    else:
        sys.exit("Error! Invalid currency code(s)!")

def getApiContentAsJson(args):
    apiUrl = "https://api.exchangeratesapi.io/latest?base="+args.base.upper()+"&symbols="+args.target.upper()
    request = Request(apiUrl)

    try:
        response = urlopen(request).read()
    except HTTPError as err:
        print("HTTPError with code:", err.code)
        sys.exit("Please check parameters!")
    except URLError as err:
        print("URLError with reason:", err.reason)
        sys.exit("Please check URL!")
    else:
        return json.loads(response.decode('utf-8'))

def getExchangeRate(content, args):
    return content['rates'][args.target.upper()]

def isValidCurrency(currency):
    isValid = False
    allowed = ['EUR', 'USD', 'CAD', 'HKD', 'ISK', 'PHP', 'DKK', 'HUF', 'CZK', 
        'AUD', 'RON', 'SEK', 'IDR', 'INR', 'BRL', 'RUB', 'HRK', 'JPY', 'THB', 
        'CHF', 'SGD', 'PLN', 'BGN', 'TRY', 'CNY', 'NOK', 'NZD', 'ZAR', 'MXN', 
        'ILS', 'GBP', 'KRW', 'MYR']
    if currency.upper() in allowed:
        isValid = True
    
    return isValid

if __name__ == '__main__':
    main()
