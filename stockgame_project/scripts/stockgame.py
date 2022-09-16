from urllib.error import HTTPError
from stockgame_functions import *
import pandas as pd
import json
from datetime import date
from datetime import timedelta
from stock_array import extract_stock_tickers
import time

RSI_THRESHOLD = 33
MINUS_DAYS = 7

def write_to_json(winner_dict, json_file):
    with open(json_file, 'r+') as file:
        json_data = json.load(file)
        json_data['winners_entries'].append(winner_dict)
        file.seek(0)
        json.dump(json_data, file, indent=4)

def get_points_of_stock(csv_path):
    is_buyable = True
    market_data_df = pd.read_csv(csv_path)
    market_data_df['Date'] = pd.to_datetime(market_data_df['Date']).dt.date

    # Find analyse values
    support_price = market_data_df['Low'].mean() # Dips under, good buy
    resistance_price = market_data_df['High'].mean() # Goes over, time to sell
    average_volume = market_data_df['Volume'].mean()
    average_change_close = market_data_df['Close'].diff()
    number_of_days = len(market_data_df.index)
    average_gain_close = average_change_close[average_change_close >= 0].sum() / number_of_days
    average_loss_close = average_change_close[average_change_close <= 0].sum() / number_of_days

    # Get calculated points
    close_price = market_data_df['Close'].iloc[-1]
    volume_today = market_data_df['Volume'].iloc[-1]
    rsi = get_rsi(average_gain_close, average_loss_close)
    if rsi < 0:
        rsi = 1
    stock_info_dict = {
            'close_price' : close_price,
            'volume_today' : int(volume_today),
            'support_price' : support_price,
            'resistance_price' : resistance_price,
            'average_volume' : average_volume,
            'average_gain_percent' : average_gain_close,
            'average_loss_percent' : average_loss_close,
            'RSI' : rsi
        }
    if (rsi > 70 or (close_price > resistance_price and average_loss_close != 0)):
        is_buyable = False
        stock_info_dict['total_points'] = -1000
        return stock_info_dict
    if (is_buyable):
        rsi_points = calc_rsi_points(rsi, RSI_THRESHOLD)
        support_points = calc_support_points(close_price, support_price)
        percent_change_close = market_data_df['Close'].pct_change()
        average_change_percent_close = percent_change_close.mean()
        apcc_points = calc_apcc_points(average_change_percent_close, average_volume, volume_today)
        total_points = rsi_points + support_points + apcc_points
        # Debug, print out points
        # print('RSI: ' + str(rsi))
        # print('RSI-Points: ' + str(rsi_points))
        # print('Support: ' + str(support_points))
        # print('APCC: ' + str(apcc_points))
        # print('Total: ' + str(total_points))
        stock_info_dict['total_points'] = total_points
        return stock_info_dict

def main():
    number_of_stocks = 20
    winner_point_array = [0] * number_of_stocks
    winner_name_array = [0] * number_of_stocks
    winner_other_info = [0] * number_of_stocks
    today = date.today()
    end_date = int(time.mktime(today.timetuple()))
    start_date = int(time.mktime((today - timedelta(days=MINUS_DAYS)).timetuple()))
    query = 'https://query1.finance.yahoo.com/v7/finance/download/{}?period1=' + str(start_date) + '&period2=' + str(end_date) + '&interval=1d&events=history&includeAdjustedClose=true'
    stock_tickers = extract_stock_tickers()
    for i in range(len(stock_tickers)):
        lowest_point = winner_point_array.index(min(winner_point_array))
        try:
            stock_dict = get_points_of_stock(query.format(stock_tickers[i]))
        except HTTPError as err:
            if err.code == 404:
                print('ERROR: ' + str(stock_tickers[i]))
                stock_dict['total_points'] = -1000
        time.sleep(1)
        print(str(i) + ': Stock point gotten from ' + stock_tickers[i] + ', points: ' + str(stock_dict['total_points']))
        if stock_dict['total_points'] > winner_point_array[lowest_point]:
            winner_point_array[lowest_point] = stock_dict['total_points']
            winner_name_array[lowest_point] = stock_tickers[i]
            winner_other_info[lowest_point] = stock_dict
    winner_dict = { }
    today = date.today().strftime('%d/%m/%Y')
    winner_dict['entry'] = {'date' : today }
    for i in range(len(winner_point_array)):
        winner_dict['entry'][('stock' + str(i))] = {}
        winner_dict['entry'][('stock' + str(i))]['stock_name'] = winner_name_array[i]
        winner_dict['entry'][('stock' + str(i))]['point_info'] = winner_other_info[i]
        winner_dict['entry'][('stock' + str(i))]['total_points'] = winner_point_array[i]
    write_to_json(winner_dict, 'stockgame_project/winners.json')
if __name__ == '__main__':
    main()