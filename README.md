# Sample_Momentum_Trading_Program
Sample Momentum Trading Program with IEX's sandbox dataset.

IEX's API uses random data, so the price information is not correct.

Dependencies to install:
```
pip install pandas
pip install numpy
pip install XlsxWriter
```

Bug Book:

1. When I tried to commit, it had problems with the .csv file with the list of names. the error read as:
```
fatal: CRLF would be replaced by LF in data/sp_500_stocks.csv
```
This was resolved by typing the following into the terminal:
```
git config core.autocrlf false
```