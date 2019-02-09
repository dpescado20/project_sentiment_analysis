import dash
import dash_core_components as dcc
import dash_html_components as html

import dash_bootstrap_components as dbc

import pandas as pd

from apps import component

app = dash.Dash(external_stylesheets=[dbc.themes.MATERIA, dbc.themes.GRID])
server = app.server

app.layout = html.Div(
    [
        component.navbar,
        html.Br(),
        dbc.Container(
            [
                component.jumbotron,
                html.Br()
            ]
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
