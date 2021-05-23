import datetime


stock_codes = {"bitcoin": "BTC-USD", "ethereum": "ETH-USD",
               'Roku, Inc':'ROKU', 'Spotify Technology S.A':'SPOT',
               'Datadog, Inc' :'DDOG', 'CrowdStrike Holdings, Inc':'CRWD', 'Tesla, Inc': 'TSLA'}

params = {
    "START_DATE": datetime.datetime(2020, 1, 1),
    "END_DATE": datetime.datetime(2021, 1, 1),
    "STOCK_CODES": stock_codes,
    "STYLE_SHEET": ["https://codepen.io/chriddyp/pen/bWLwgP.css"],
}
