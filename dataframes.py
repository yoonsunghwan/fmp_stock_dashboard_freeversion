import pandas as pd
import fmpsdk
import configparser

config = configparser.ConfigParser()
config.read('ak.cfg')
fmp_key = config.get('access_key','FMP_ACCESS_KEY')
symbol = 'aapl'



def daily_adjusted_df(apikey, symbol, ohlc, start , end):

    df = pd.DataFrame(fmpsdk.historical_price_full(apikey=apikey, symbol= symbol, from_date= start, to_date= end)['historical'])[['date',ohlc,'volume']]

    return df






