import plotly.graph_objs as go
import yfinance as yf

data = yf.Ticker("ITSA4.SA").history("max")

fig = go.Figure()

fig.add_trace(go.Candlestick(x=data.index,open = data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name = 'market data'))

fig.update_layout(title = 'Papel', yaxis_title = 'Preço')

fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label='1d', step='day', stepmode='backward'),
            dict(count=7, label='1wk', step='day', stepmode='backward'),
            dict(count=14, label='2wk', step='day', stepmode='backward'),
            dict(count=1, label='1mo', step='month', stepmode='backward'),
            dict(count=1, label='1y', step='year', stepmode='backward'),
            dict(step='all')
            ])
    )
)

fig.show()
#fig.to_html()



## for django...

#graph = fig.to_html(full_html=False, default_height=500, default_width=700)
#
#context = {'graph': graph}
#response = render(request, 'graph.html', context)





## only some select stocks...... =/

#import plotly.express as px
#
#df = px.data.stocks()
#fig = px.line(df, x='date', y="GOOG")
#fig.show()
