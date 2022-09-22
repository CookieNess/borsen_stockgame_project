import mysql.connector
from mysql.connector import Error
from getpass import getpass
import time
from datetime import date
from datetime import timedelta
from utils.stock_array import extract_stock_tickers


def insert_into_table_prices(cursor, yahoo_ticker, date, open, high, low, close, volume):
    print('hello')

def main():
    db_password = getpass(prompt="DB Password: ")
    connection = mysql.connector.connect(host='localhost', database='stockgamedb',user='root',password=db_password)
    cursor = connection.cursor()
    today = date.today()
    end_date = int(time.mktime(today.timetuple()))
    start_date = int(time.mktime((today - timedelta(days=365)).timetuple()))
    query = 'https://query1.finance.yahoo.com/v7/finance/download/{}?period1=' + str(start_date) + '&period2=' + str(end_date) + '&interval=1d&events=history&includeAdjustedClose=true'
    stock_tickers = extract_stock_tickers()
    print(stock_tickers)
    cursor.close()
    connection.close()



if __name__ == '__main__':
    main()