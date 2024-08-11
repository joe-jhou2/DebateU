from dash import Dash, dcc, html
import random

def build_content(mysql):
    keywords = mysql.execute_query("select name from keyword order by name")
    options = [k[0] for k in keywords]
    random_topic = random.choice(options)
    return html.Div([
        html.H5("Select a topic for discussion"),
        dcc.Dropdown( options,
            id='select_debate_topic_dropdown',
            value=random_topic,
            style={'width': '50%', 'backgroundColor': 'white', 'textAlign': 'center', 'margin': 'auto'},

        )
    ], style={'width': '100%', 'marginBottom': '20px', 'padding': '10px', 'boxSizing': 'border-box', 'border': '1px solid #ccc', 'backgroundColor': 'lightgrey'})
