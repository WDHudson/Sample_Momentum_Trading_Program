import numpy as np
import pandas as pd
import requests
import math
from scipy.stats import percentileofscore as score
import xlsxwriter
from secrets import IEX_CLOUD_API_TOKEN
from helpers import chunks


stocks = pd.read_csv('sp_500_stocks.csv')

portfolio_size = 1000000
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

# Loop through all the symbols in the symbol string object
for symbol in symbol_string:
  # Create a batch API request for each group of 100 symbols
  batch_api_url = f'https://sandbox.iexapis.com/stable/stock/market/batch/?types=stats,quote&symbols={symbol}&token={IEX_CLOUD_API_TOKEN}'
  # Declaring the variable of the response of the API request in json format
  data = requests.get(batch_api_url).json()
  # Breaking down each individual ticker from each batch of 100 tickers and all of their data
  for ticker in symbol.split(','):
    # Appending to the final dataframe
    final_dataframe = final_dataframe.append(
      pd.Series(
        [
          # Needs to fill in 4 columns, so the N/A is just a place holder for the time being
          ticker,
          data[ticker]['quote']['iexRealtimePrice'],
          data[ticker]['stats']['year1ChangePercent'],
          'N/A'
        ],
        index = my_columns
      ),
      ignore_index = True
    )

# Sorts the dataframe by One Year Return. ascending = False puts the highest values on top and the inplace = True modifies the existing dataframe
final_dataframe.sort_values('One Year Return', ascending = False, inplace = True)
# Remove the low momentum stocks from the data frame
final_dataframe = final_dataframe[:50]
# inplace = True is used to modify the existing dataframe
final_dataframe.reset_index(inplace = True)

position_size = float(portfolio_size) / len(final_dataframe.index)
for i in range(0, len(final_dataframe['Ticker'])):
  # Insert in column with header Number of Shares to Buy the value of 1/ 50th of the portfolio divided by the share price
  final_dataframe.loc[i, 'Number of Shares to Buy'] = position_size / final_dataframe['Price'][i]

hqm_columns = [
  'Ticker',
  'Price',
  'Number of Shares to Buy',
  '1 Year Price Return',
  '1 Year Return Percentile',
  '6 Month Price Return',
  '6 Month Return Percentile',
  '3 Month Price Return',
  '3 Month Return Percentile',
  '1 Month Price Return',
  '1 Month Return Percentile'
  ]

hqm_dataframe = pd.DataFrame(columns = hqm_columns)

for symbol in symbol_string:
  batch_api_url = f'https://sandbox.iexapis.com/stable/stock/market/batch/?types=stats,quote&symbols={symbol}&token={IEX_CLOUD_API_TOKEN}'
  data = requests.get(batch_api_url).json()
  for ticker in symbol.split(','):
    hqm_dataframe = hqm_dataframe.append(
      pd.Series(
        [
          ticker,
          data[ticker]['quote']['iexRealtimePrice'],
          'N/A',
          data[ticker]['stats']['year1ChangePercent'],
          'N/A',
          data[ticker]['stats']['month6ChangePercent'],
          'N/A',
          data[ticker]['stats']['month3ChangePercent'],
          'N/A',
          data[ticker]['stats']['month1ChangePercent'],
          'N/A'
        ],
        index = hqm_columns
      ),
      ignore_index = True
    )

time_periods = [
  '1 Year',
  '6 Month',
  '3 Month',
  '1 Month'
]

for row in hqm_dataframe.index:
  for time_period in time_periods:
    percentile_return = f'{time_period} Return Percentile'
    price_return = f'{time_period} Price Return'
    # Score is defined at top of page from an import of scipy
    hqm_dataframe.loc[row, percentile_return] = score(hqm_dataframe[price_return], hqm_dataframe.loc[row, price_return]) / 100

print(hqm_dataframe)