import numpy as np
import pandas as pd
import requests
import math
from scipy import stats
import xlsxwriter
from secrets import IEX_CLOUD_API_TOKEN


stocks = pd.read_csv('sp_500_stocks.csv')

symbol = 'AAPL'
api_url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/stats?token={IEX_CLOUD_API_TOKEN}'

data = requests.get(api_url)

print(data)