import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, html, Input, Output
from ta.trend import MACD
from core.patterns import detect_all_patterns
from core.utils import generate_levels, generate_trendlines, calculate_probabilities


def get_chart(df, levels, trendlines, entry=None, sl=None, tp=None):
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df.index,
                                 open=df['Open'],
                                 high=df['High'],
                                 low=df['Low'],
                                 close=df['Close'], name='Bougies'))

    for level in levels:
        fig.add_hline(y=level, line_dash="dot", line_color="gray")

    for trendline in trendlines:
        fig.add_trace(go.Scatter(x=[p[0] for p in trendline], y=[p[1] for p in trendline], mode='lines', line=dict(dash="dash"), name="Tendance"))

    if entry and sl and tp:
        fig.add_hline(y=entry, line_color="blue", annotation_text="Entrée", line_dash="dot")
        fig.add_hline(y=sl, line_color="red", annotation_text="SL", line_dash="dash")
        fig.add_hline(y=tp, line_color="green", annotation_text="TP", line_dash="dash")

    fig.update_layout(template="plotly_dark", height=600)
    return fig


analyze_layout = html.Div([
    html.H3("Analyse Technique"),
    dcc.Dropdown(id='pair', options=[
        {'label': 'EUR/USD', 'value': 'EURUSD=X'},
        {'label': 'BTC/USD', 'value': 'BTC-USD'},
        {'label': 'ETH/USD', 'value': 'ETH-USD'},
        {'label': 'GBP/USD', 'value': 'GBPUSD=X'}
    ], value='EURUSD=X'),
    dcc.Dropdown(id='timeframe', options=[
        {'label': '1h', 'value': '60m'},
        {'label': '4h', 'value': '240m'},
        {'label': '1j', 'value': '1d'}
    ], value='60m'),
    html.Button("Analyser", id='analyze-btn'),
    html.Div(id='analysis-output'),
    dcc.Graph(id='chart')
])


def register_callbacks(app):
    @app.callback(
        [Output('analysis-output', 'children'),
         Output('chart', 'figure')],
        [Input('analyze-btn', 'n_clicks')],
        [dash.State('pair', 'value'), dash.State('timeframe', 'value')]
    )
    def update_analysis(n, pair, tf):
        if not n:
            return dash.no_update

        df = yf.download(pair, period="3mo", interval=tf)
        df.dropna(inplace=True)
        macd = MACD(close=df['Close']).macd_diff()

        signal = "MACD haussier" if macd.iloc[-1] > 0 else "MACD baissier"
        last_price = df['Close'].iloc[-1]
        sl = round(last_price * 0.99, 2)
        tp = round(last_price * 1.02, 2)
        rr = round((tp - last_price) / (last_price - sl), 2)

        patterns = detect_all_patterns(df)
        levels = generate_levels(df)
        trends = generate_trendlines(df)
        proba = calculate_probabilities(patterns)

        fig = get_chart(df, levels, trends, entry=last_price, sl=sl, tp=tp)

        summary = html.Div([
            html.P(f"Entrée : {last_price} | SL : {sl} | TP : {tp}"),
            html.P(f"Risque/Rendement : {rr}"),
            html.P(f"Probabilité de réussite : {proba}%"),
            html.P(f"{signal}"),
            html.Hr(),
            html.H5("Patterns détectés :"),
            html.Ul([html.Li(p) for p in patterns])
        ])

        return summary, fig
