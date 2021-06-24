import numpy as np
import pandas as pd
import requests
import math
from scipy.stats import percentileofscore as score
import xlsxwriter
from secrets import IEX_CLOUD_API_TOKEN
from helpers import chunks
from statistics import mean
from excel_formats import string_format, dollar_format, integer_format, column_formats, writer

portfolio_value = 1000000

stocks = pd.read_csv('sp_500_stocks.csv')

# Use imported chunks function to group API requests into groups of 100
symbol_group = list(chunks(stocks['Ticker'], 100))
# Create an empty array to push each group of tickers into
symbol_string = []
# Goes through each of the items in the list created above...
for i in range(0, len(symbol_group)):
  # ... and fill into the array just the ticker separated by a comma
  symbol_string.append(','.join(symbol_group[i]))

# Make a list of column titles
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
  '1 Month Return Percentile',
  'HQM Score'
  ]

hqm_dataframe = pd.DataFrame(columns = hqm_columns)

# Loop through all the symbols in the symbol string object
for symbol in symbol_string:
  # Create a batch API request for each group of 100 symbols
  batch_api_url = f'https://sandbox.iexapis.com/stable/stock/market/batch/?types=stats,quote&symbols={symbol}&token={IEX_CLOUD_API_TOKEN}'
  # Declaring the variable of the response of the API request in json format
  data = requests.get(batch_api_url).json()
  # Breaking down each individual ticker from each batch of 100 tickers and all of their data
  for ticker in symbol.split(','):
    # Appending to the hqm dataframe
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
          'N/A',
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
    hqm_dataframe.loc[row, percentile_return] = score(hqm_dataframe[price_return], hqm_dataframe.loc[row, price_return])

for row in hqm_dataframe.index:
  momentum_percentiles = []
  for time_period in time_periods:
    momentum_percentiles.append(hqm_dataframe.loc[row, f'{time_period} Return Percentile'])
  hqm_dataframe.loc[row, 'HQM Score'] = mean(momentum_percentiles)

hqm_dataframe.sort_values('HQM Score', ascending = False, inplace = True)
hqm_dataframe = hqm_dataframe[:50]
# drop = True refers to removing the old index and replacing with a new one
hqm_dataframe.reset_index(inplace = True, drop = True)

position_size = float(portfolio_value) / len(hqm_dataframe.index)

for i in hqm_dataframe.index:
  hqm_dataframe.loc[i, 'Number of Shares to Buy'] = math.floor(position_size / hqm_dataframe.loc[i, 'Price'])

# Create Excel Book
hqm_dataframe.to_excel(writer, sheet_name='Recommended Trades', index = False)

for column in column_formats.keys():
  writer.sheets['Recommended Trades'].set_column(f'{column}:{column}', 20, column_formats[column][1])
  writer.sheets['Recommended Trades'].write(f'{column}1', column_formats[column][0], string_format)

writer.save()