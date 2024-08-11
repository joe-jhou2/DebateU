from dash import Dash, dcc, html

def build_content(home: int, visitors: int) -> html.Div:
    return html.Div([
        html.Div([
            html.Div(home, id="score_0", className="score", style={'fontSize': '60px', 'textAlign': 'center'}),
        ], style={'width': '50%', 'backgroundColor': 'lightblue', 'float': 'left', 'height': '100%'}),
        html.Div([
            html.Div(visitors, id="score_1", className="score", style={'fontSize': '60px', 'textAlign': 'center'}),
        ], style={'width': '50%', 'backgroundColor': 'pink', 'float': 'left', 'height': '100%'}),
    ], className="score-widget", style={'width': '100%', 'height': '92px'})

