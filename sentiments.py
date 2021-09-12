import pandas as pd
import fmpsdk
import configparser
import streamlit as st
config = configparser.ConfigParser()
config.read('ak.cfg')
fmp_key = config.get('access_key','FMP_ACCESS_KEY')
symbol = 'aapl'

def get_news(apikey, tickers):
    news = fmpsdk.stock_news(apikey=fmp_key,tickers =symbol,limit = 100)
    for n in news:
        st.write(n['site'])
        st.write(n['publishedDate'])
        link = f'[[{n["title"]}]({n["url"]})'
        st.markdown(link, unsafe_allow_html=True)
