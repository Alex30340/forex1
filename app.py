from dash import Dash, dcc, html, page_container
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.DARKLY])

app.layout = html.Div([
    dcc.Location(id="url"),
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Accueil", href="/")),
            dbc.NavItem(dbc.NavLink("Analyse", href="/analyse")),
            dbc.NavItem(dbc.NavLink("Dashboard", href="/dashboard")),
            dbc.NavItem(dbc.NavLink("Backtest", href="/backtest")),
            dbc.NavItem(dbc.NavLink("Éducation", href="/education")),
            dbc.NavItem(dbc.NavLink("LAB", href="/lab")),
        ],
        brand="Forex Analyzer",
        color="dark",
        dark=True,
    ),
    page_container
])

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
