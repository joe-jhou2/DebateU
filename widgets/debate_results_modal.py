import dash_bootstrap_components as dbc
from dash import Dash, html
from adapters.mysql_adapter import MySQLDatabase
from game.game import Game


def getModal(mysql: MySQLDatabase):
    return dbc.Modal([
        dbc.ModalHeader([
            html.H1("Debate results"),
        ], style={'textAlign': 'center'}, close_button=False),
        dbc.ModalBody([

            html.H1(id="univer_winner"),
            html.Img(id="univer_winner_logo", style={'width': '100%'}),
            html.H2(id="player_winner"),
            html.Img(id="player_winner_logo", style={'width': '100%'}),
            html.H3("Result Explanation:"),
            html.Ul([
                html.Li([
                    html.P([
                        html.Strong([
                            html.Div(id="faculty_interest_explanation")
                        ])
                    ])]),
                html.Li([
                    html.P([
                        html.Strong([
                            html.Div(id="faculty_publications_explanation")
                        ])
                    ])]),
                html.Li([
                    html.P([
                        html.Strong([
                            html.Div(id="faculty_relation_explanation")
                        ])
                    ])]),
                ], id="result_explanation"),
            html.Button("Close", id="close_modal", n_clicks=0, style={'width': '100%'})
        ])
    ], id="modal", centered=True, is_open=False)
