import pandas_datareader.data as web
import datetime
import dtale

start = datetime.datetime(2019, 1, 1)
end = datetime.datetime(2021,1,1)

bitcoin  = web.get_data_yahoo('BTC-USD', start=start, end=end)
ethereum = web.get_data_yahoo('ETH-USD', start=start, end=end)


