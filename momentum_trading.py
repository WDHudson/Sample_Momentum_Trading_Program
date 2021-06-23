import numpy as np
import pandas as pd
import requests
import math
from scipy import stats
import xlsxwriter
from secrets import IEX_CLOUD_API_TOKEN
from helpers import chunks


stocks = pd.read_csv('sp_500_stocks.csv')


# data = requests.get(api_url).json()

# Use imported chunks function to group API requests into groups of 100
symbol_group = list(chunks(stocks['Ticker'], 100))
# Create an empty array to push each group of tickers into
symbol_string = []
# Goes through each of the items in the list created above...
for i in range(0, len(symbol_group)):
  # ... and fill into the array just the ticker separated by a comma
  symbol_string.append(','.join(symbol_group[i]))

# Make a list of column titles
my_columns = ['Ticker', 'Price', 'One Year Return', 'Number of Shares to Buy']

# Create a blank Data Frame
final_dataframe = pd.DataFrame(columns = my_columns)

for symbol in symbol_string:
  batch_api_url = f'https://sandbox.iexapis.com/stable/stock/market/batch/?types=stats,quote&symbols={symbol}&token={IEX_CLOUD_API_TOKEN}'
  data = requests.get(batch_api_url).json()
  for ticker in symbol.split(','):
    final_dataframe = final_dataframe.append(
      pd.Series(
        [
          ticker,
          data[ticker]['quote']['iexRealtimePrice'],
          data[ticker]['stats']['year1ChangePercent'],
          'N/A'
        ],
        index = my_columns
      ),
      ignore_index = True
    )

print(final_dataframe)