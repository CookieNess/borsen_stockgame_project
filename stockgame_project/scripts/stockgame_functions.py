def get_rsi(average_gain_close, average_loss_close):
    if average_gain_close == 0:
        return 100
    elif average_loss_close == 0:
        return 1
    else:
        rs = average_gain_close / (average_loss_close*-1)
        rsi = 100 - (100 / (1 + rs))
        return rsi

def calc_rsi_points(rsi, RSI_THRESHOLD):
    if (rsi < RSI_THRESHOLD):
        change = RSI_THRESHOLD - rsi
        return ((change/rsi) * 100)
    else:
        return 0

def calc_support_points(close_price, support_price):
    if (close_price < (support_price * 1.01)):
        change = support_price - close_price
        return ((change/close_price) * 100)
    else:
        return 0

def calc_apcc_points(average_percent_change_close, average_volume, volume_today):
    change = volume_today - average_volume
    return ((change/average_volume) * 100) + average_percent_change_close



