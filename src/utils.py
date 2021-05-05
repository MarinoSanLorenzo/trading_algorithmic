import pandas_datareader.data as web

__all__ = ['get_data']

def get_data(params:dict, stocks:list) -> dict:
    '''
    Fetch the data
    :param params:
    :param stocks: list of the selected stocks
    :return: dictionary with the dataframe as value per key stock
    '''
    stock_codes = params.get('STOCK_CODES')
    start = params.get('START_DATE')
    end = params.get('END_DATE')
    data = {}
    for name, code in stock_codes.items():
        if name in stocks:
            data[name] = web.get_data_yahoo(code, start=start, end=end)
    return data


