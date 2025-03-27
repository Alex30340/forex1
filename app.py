from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import dash

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.DARKLY])

app.layout = dbc.Container([
    dcc.Location(id="url"),
    dash.page_container
], fluid=True)

if __name__ == "__main__":
    app.run(debug=True)
