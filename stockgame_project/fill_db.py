import mysql.connector
from mysql.connector import Error
from getpass import getpass
import time
from datetime import date
from datetime import timedelta
from utils.stock_array import extract_stock_tickers
import pandas as pd
from urllib.error import HTTPError


def insert_into_table_prices(cursor, yahoo_ticker, date, open, high, low, close, volume):
    insert_price_query = "INSERT INTO Prices(YahooTicker, DateRecorded,OpenPrice,HighPrice,LowPrice,ClosePrice,Volume) VALUES(%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(insert_price_query, (yahoo_ticker, date, open, high, low, close, volume))
def main():
    db_password = getpass(prompt="DB Password: ")
    connection = mysql.connector.connect(host='localhost', database='stockgamedb',user='root',password=db_password)
    cursor = connection.cursor()
    today = date.today()
    end_date = int(time.mktime(today.timetuple()))
    start_date = int(time.mktime((today - timedelta(days=365)).timetuple()))
    query = 'https://query1.finance.yahoo.com/v7/finance/download/{}?period1=' + str(start_date) + '&period2=' + str(end_date) + '&interval=1d&events=history&includeAdjustedClose=true'
    stock_tickers = extract_stock_tickers()
    for i in range(len(stock_tickers)):
        error_ticker = False
        try:
            stock_prices = pd.read_csv(query.format(stock_tickers[i]))
        except HTTPError as err:
            print('ERROR ' + str(stock_tickers[i]))
        try:
            cursor.execute("INSERT INTO Tickers VALUES(%s)", (stock_tickers[i],))
        except:
            print('ERROR inserting ticker: ' + str(stock_tickers[i]))
            error_ticker = True
        for index, row in stock_prices.iterrows():
            if (error_ticker):
                pass
            else:
                try:
                    insert_into_table_prices(cursor, stock_tickers[i], row.Date, row.Open, row.High, row.Low, row.Close, row.Volume)
                except:
                    pass
        print("Inserted stock: " + str(stock_tickers[i]))
        time.sleep(1)
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == '__main__':
    main()