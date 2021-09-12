from fbprophet.plot import plot_components_plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pytrends.request import TrendReq
from fbprophet import Prophet
import fmpsdk
import pandas as pd
from fbprophet.plot import plot_plotly


def daily_graph(df, symbol, ohlc):

    # Create subplots and mention plot grid size
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        vertical_spacing=.08, subplot_titles=(f'Historically Adjusted Closing Prices for: {symbol}', 'Volume'),
                        row_width=[.3, 1])

    # Plot OHLC on 1st row
    fig.add_trace(go.Scatter(x=df['date'], y=df[ohlc], showlegend=False,),row=1, col=1
                  )

    # Bar trace for volumes on 2nd row without legend
    fig.add_trace(go.Bar(x=df['date'], y=df['volume'], showlegend=False), row=2, col=1)

    # Do not show OHLC's rangeslider plot
    fig.update(layout_xaxis_rangeslider_visible=False)
    fig.update_layout(height=800, yaxis_title = 'Price ($)')

    return fig

def intra_day_graph(apikey, symbol, time_delta, ohlc):
    if ohlc == 'adjClose':
        return "Adjusted Closing Price is not available for intraday data, please choose a different OHLC."
    df = pd.DataFrame(fmpsdk.historical_chart(apikey, symbol, time_delta))[['date', ohlc,'volume']]

    # Create subplots and mention plot grid size
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        vertical_spacing=.08, subplot_titles=(f'Historically Adjusted Closing Prices for: {symbol}', 'Volume'),
                        row_width=[.3, 1])

    # Plot OHLC on 1st row
    fig.add_trace(go.Scatter(x=df['date'], y=df[ohlc], showlegend=False, mode='markers', ),row=1, col=1
                  )

    # Bar trace for volumes on 2nd row without legend
    fig.add_trace(go.Bar(x=df['date'], y=df['volume'], showlegend=False,), row=2, col=1)

    # Do not show OHLC's rangeslider plot
    fig.update(layout_xaxis_rangeslider_visible=False)
    fig.update_layout(height=800,yaxis_title = 'Price ($)')

    return fig
    #
    # df = pd.DataFrame(fmpsdk.historical_chart(apikey, symbol, time_delta))[['date', ohlc]]
    # df['date'] = pd.DatetimeIndex(df['date'])
    # fig = px.scatter(df.set_index('date'), trendline='lowess', labels={'value': "Price ($)", 'date': ''})
    # fig.update_layout(dict1={'title': f'Price Action for:  {symbol}'}, showlegend=False)
    # return fig

def trends_line_plot(symbol,timeframe):
    """

    :param symbol: symbol of security ("AAPL")
    :param timeframe: '{start} {end}'
    :return: plotly line graph
    """

    symbol = f'{symbol} stock'
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(kw_list=[symbol], timeframe=timeframe)

    trends_over_time = pytrends.interest_over_time().drop('isPartial', axis=1)
    fig = px.line(trends_over_time, labels={'value': "Interest Score", 'date': ''})
    fig.update_layout(dict1={'title': f'Google Search Interest Over Time for:  {symbol}'}, showlegend=False)
    fig.update_yaxes(title='Interest')

    return fig

def prophet_forecast(df, periods, ohlc):
    """
    :param df: daily_adjusted dataframe retrieved from fmp
    :return: forecasted, trends
    """
    model = Prophet()
    #keep just the date and adjusted close and rename to ds and y
    df = df.rename({'date':'ds',ohlc:'y'}, axis = 1)[['ds','y']]

    model.fit(df)

    future = model.make_future_dataframe(periods=periods, include_history=False)
    forecast = model.predict(future)
    forecasted_plot = plot_plotly(model,forecast, xlabel ='',ylabel = 'Price ($)')
    components_plot = plot_components_plotly(model, forecast)

    return forecasted_plot, components_plot

def financial_graphs(df,col_names, title):
    fig = go.Figure()
    for col_name in col_names:
        fig.add_trace(go.Scatter(x=df.index, y=df[col_name],
                             mode='lines+markers',
                             name=col_name))
    fig.update_layout(title ={'text':title})

    return fig