from flask import Flask
from dash import Dash
import dash_bootstrap_components as dbc
from sentiment.api.routes import app_api

server = Flask(__name__)
server.register_blueprint(app_api)

dashapp = Dash(__name__,
               server=server,
               external_stylesheets=[dbc.themes.MATERIA],
               url_base_pathname='/')

from sentiment.site.dashboard import *
