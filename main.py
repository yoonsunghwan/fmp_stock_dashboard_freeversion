import streamlit as st
import plotly_graphs
import requests
import pandas as pd
import fmpsdk
from dataframes import daily_adjusted_df
from datetime import datetime, timedelta
import screener
#import configparser
#from .. import get_news
st.set_page_config(page_title='Stock Dashboard', layout='wide', initial_sidebar_state="expanded")

#config = configparser.ConfigParser()
#config.read('ak.cfg')

#change if running from my computer
#fmp_key = config.get('access_key','FMP_ACCESS_KEY')
#alpha_key = config.get('access_key','ALPHA_ACCESS_KEY')

fmp_key = st.secrets['fmp_key']
alpha_key = st.secrets['alpha_key']

period = 'yearly'

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
st.title('Stock Picking Tool')


option = st.sidebar.selectbox('Choose type of analysis', ['Screener', 'Dashboard','Company Profile','News','Sentimental','Historical', 'Forecasting'])
symbol = st.sidebar.text_input('Input Symbol','CRSR').upper()
try:
    comp_prof = fmpsdk.company_profile(apikey=fmp_key, symbol=symbol)[0]
    start = st.sidebar.date_input('Start', datetime.today() - timedelta(90),  min_value=datetime.strptime(comp_prof['ipoDate'],'%Y-%m-%d')\
                              , max_value = datetime.today() - timedelta(1))
    end = st.sidebar.date_input('End', max_value=datetime.today())
    ohlc = st.sidebar.selectbox('Pick OHLC', ('open', 'high', 'low', 'close', 'adjClose'))
except IndexError:
    warning_message = st.warning(f'{symbol} is not a company, cannot get company profile, try looking at the historical charts.')
    start = st.sidebar.date_input('Start', datetime.today() - timedelta(90)\
                              , max_value = datetime.today() - timedelta(1))
    end = st.sidebar.date_input('End', max_value=datetime.today())
    ohlc = st.sidebar.selectbox('Pick OHLC', ('open', 'high', 'low', 'close', 'adjClose'))

if option == 'Dashboard':
    #cash flow
    st.subheader(f'Cash Flow Statement for {symbol}')
    cash_flow = pd.DataFrame(fmpsdk.cash_flow_statement(fmp_key, symbol, period=period, limit=None))
    cash_flow.index = pd.DatetimeIndex(cash_flow['date'])
    st.dataframe(cash_flow)
    cf_col_names = list(cash_flow.select_dtypes(exclude = 'object').columns)
    cf_col_name = st.multiselect('Choose columns for the cash flow graph',cf_col_names,['netIncome','freeCashFlow'])
    st.plotly_chart(plotly_graphs.financial_graphs(df=cash_flow,col_names=cf_col_name, title = "cash flow"), use_container_width=True)

    st.subheader(f'Balance Sheet for {symbol}')
    balance_sheet = pd.DataFrame(fmpsdk.balance_sheet_statement(fmp_key, symbol, period=period, limit=None))
    balance_sheet.index = pd.DatetimeIndex(balance_sheet['date'])
    st.dataframe(balance_sheet)
    bs_col_names = list(balance_sheet.select_dtypes(exclude= 'object').columns)
    bs_col_name = st.multiselect('Choose column for the balance sheet graph',bs_col_names,['netDebt','totalCurrentAssets'])
    st.plotly_chart(plotly_graphs.financial_graphs(df=balance_sheet, col_names=bs_col_name, title= "balance sheet"), use_container_width=True)

    st.subheader(f'Income statement for {symbol}')
    income_statement = pd.DataFrame(fmpsdk.income_statement(fmp_key, symbol, period=period, limit=None))
    income_statement.index= pd.DatetimeIndex(income_statement['date'])
    st.dataframe(income_statement)
    is_col_names = list(income_statement.select_dtypes(exclude='object').columns)
    is_col_name  = st.multiselect('Choose column for the income statement graph', is_col_names, ['revenue','grossProfit'])
    st.plotly_chart(plotly_graphs.financial_graphs(df=income_statement, col_names=is_col_name, title= "income statement"), use_container_width=True)

    #investing
    #financing

if option == 'Screener':
    st.subheader("Stock Screener")
    #values for drop down list
    sector = screener.sector
    industry = screener.industry
    exchange = screener.exchange

    #create containers for columns
    r1_c1, r1_c2, r1_c3 = st.columns((1,1.5,1.5))
    r2_c1, r2_c2, r2_c3 = st.columns((1,1.5,1.5))
    r3_c1, r3_c2, r3_c3 = st.columns((1,1.5,1.5))
    r4_c1, r4_c2, r4_c3 = st.columns((1,1.5,1.5))

    #row 1 cols 1,2,3
    exchange_value = r1_c1.multiselect('Exchange',exchange, ['NYSE','NASDAQ'])
    m_min, m_max = r1_c2.number_input('Market Cap More Than', 0), r1_c3.number_input('Market Cap Less Than', 0)
    #row 2, cols 1,2,3
    sector_value = r2_c1.selectbox('Sector', sector,)
    v_min, v_max = r2_c2.number_input('Volume More Than', 0), r2_c3.number_input('Volume Less Than', 0)
    #row 3, cols 1,2,3
    industry_value = r3_c1.selectbox('Industry', industry,)
    div_min, div_max = r3_c2.number_input('Dividend More Than', 0), r3_c3.number_input('Dividend Less Than', 0)
    #row 4. cols 1,2,3
    limit = r4_c1.number_input('Limit Query', 100)
    beta_min, beta_max = r4_c2.number_input('Beta More Than',0), r4_c3.number_input('Beta Less Than', 0)


    if st.button('press to screen'):
        with st.spinner('Screeeeeening'):
            st.dataframe(fmpsdk.stock_screener(apikey=fmp_key, exchange=exchange_value, market_cap_more_than=m_min,
                                           market_cap_lower_than=m_max, \
                                           sector=sector_value, volume_more_than=v_min, volume_lower_than=v_max,
                                           industry=industry_value, \
                                           dividend_more_than=div_min, dividend_lower_than=div_max, beta_more_than=beta_min,
                                           beta_lower_than=beta_max, limit = limit))
            st.success("finished")

try:
    daily_df = daily_adjusted_df(fmp_key, symbol, ohlc, start,end)
except KeyError:
    st.warning("Please input valid symbol")

if option == 'Company Profile':
    link = f'[{comp_prof["companyName"]}]({comp_prof["website"]})'
    st.subheader(link)
    st.write(f"{comp_prof.pop('description')}")
    st.json(comp_prof)

if option == 'Historical':

    #prepare dataframe from dataframes library
    st.subheader(f'Daily Adjusted Close for {symbol}')
    st.plotly_chart(plotly_graphs.daily_graph(daily_df ,symbol, ohlc))
    #intraday
    st.subheader(f'Intraday Data for {symbol}')
    col_td, col_ohlc = st.columns(2)
    td = col_td.selectbox('Pick Intraday Timedelta',('1min', '5min', '15min', '1hour', '4hour'))

    st.write(plotly_graphs.intra_day_graph(fmp_key,symbol,td, ohlc))



if option == 'News':
    try:
        slider_num = st.select_slider(f'Slide me to get up to 10,000 recent news for {symbol}',[1,5,10,20,50,100,200,1000,5000, 10000],5)
        slider_num =int(slider_num)
        url = f"https://financialmodelingprep.com/api/v3/stock_news?tickers={symbol}&limit={slider_num}&apikey={fmp_key}"
        resp = requests.get(url)
        news = resp.json()
        for n in news[0:slider_num]:
            st.markdown('------------------')
            st.markdown(f"**{n['site']}**")
            st.write('Published: ' + n['publishedDate'])
            link = f'[{n["title"]}]({n["url"]})'
            st.markdown(link, unsafe_allow_html=True)
            st.write(n['text'])
    except KeyError:
        st.write("Please input the stock symbol")

if option == 'Sentimental':

    #google search interest
    st.subheader(f"Google Search Interest for {symbol}")

    timeframe = f'{start} {end}'
    st.text(f""" 
                Numbers represent search interest in the USA.
                It is relative to the highest point from {start} to {end}.
                A value of 100 is the peak popularity for the term. 
                A value of 50 means that the term is half as popular. 
                A score of 0 means there was not enough data for this term.""")
    try:
        st.write(plotly_graphs.trends_line_plot(symbol=symbol,timeframe= timeframe))
    except:
        st.text("Please use a different start or end date")


if option == 'Forecasting':

    try:
        st.subheader("Forecasting with Prophet")
        days_to_future = st.text_input(f"How many days to the future do you want to forecast {symbol}?")


        periods = int(days_to_future)
        if days_to_future:
            prophet_graph = plotly_graphs.prophet_forecast(daily_df, periods, ohlc)
            st.write(prophet_graph[0])
            st.subheader("Trend Lines")
            st.write(prophet_graph[1])
    except:
        st.write("please type in the number of days")

    with st.expander(f"Click to see daily prices for {comp_prof['companyName']} from its IPO date"):
        st.plotly_chart(plotly_graphs.daily_graph(daily_adjusted_df(fmp_key, symbol,ohlc, start=None, end=None), symbol, ohlc))

