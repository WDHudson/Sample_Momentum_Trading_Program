import pandas as pd

# Initializing the XlsxWriter Object
writer = pd.ExcelWriter('recommended_trades.xlsx', engine='xlsxwriter')

# Formatting the Excel Output
background_color = '#0a0a23'
font_color = '#ffffff'


string_format = writer.book.add_format(
  {
    'font_color': font_color,
    'bg_color': background_color,
    'border': 1
  }
)

dollar_format = writer.book.add_format(
  {
    'num_format': '$0.00',
    'font_color': font_color,
    'bg_color': background_color,
    'border': 1
  }
)

integer_format = writer.book.add_format(
  {
    'num_format': '0.00',
    'font_color': font_color,
    'bg_color': background_color,
    'border': 1
  }
)

column_formats = {
  'A': ['Ticker', string_format],
  'B': ['Price', dollar_format],
  'C': ['Number of Shares to Buy', integer_format],
  'D': ['1 Year Price Return', integer_format],
  'E': ['1 Year Return Percentile', integer_format],
  'F': ['6 Month Price Return', integer_format],
  'G': ['6 Month Return Percentile', integer_format],
  'H': ['3 Month Price Return', integer_format],
  'I': ['3 Month Return Percentile', integer_format],
  'J': ['1 Month Price Return', integer_format],
  'K': ['1 Month Return Percentile', integer_format],
  'L': ['HQM Score', integer_format]
}