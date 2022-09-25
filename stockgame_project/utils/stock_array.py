from bs4 import BeautifulSoup

def extract_stock_tickers():
    with open('stockgame_project/utils/index.html', 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')
    stock_containers = soup.find_all('div', {'class' : 'top-info'})
    stock_names = [''] * len(stock_containers)
    for i in range(len(stock_containers)):
        stock_ticker = stock_containers[i].find('div', {'class' : 'top-image'}).string
        stock_exchange_yahoo = ''
        stock_exchange_original = stock_containers[i].find('div', {'class' : 'top-exchange'}).string
        if stock_exchange_original == 'CSE' or stock_exchange_original == 'XFND':
            stock_exchange_yahoo = '.CO'
        elif stock_exchange_original == 'SSE':
            stock_exchange_yahoo = '.ST'
        elif stock_exchange_original == 'HEX':
            stock_exchange_yahoo = '.HE'
        elif stock_exchange_original == 'OSE':
            stock_exchange_yahoo = '.OL'
        else:
            stock_exchange_yahoo = ''
        stock_names[i] = (stock_ticker + stock_exchange_yahoo).replace(' ', '')
    return stock_names