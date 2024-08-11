from dash import Dash, dcc, html, Input, Output
import random

def build_content(mysql, player: int) -> html.Div:
    unis = mysql.execute_query("select name, photo_url from university order by name")
    uni_names = [uni[0] for uni in unis]
    random_uni = random.choice(unis)
    return html.Div([
        html.Img(src=random_uni[1], id="university_image" + str(player), className="university-image",
                 style={'height': '70px'}),
        dcc.Dropdown(uni_names, id="select_university_dropdown" + str(player), placeholder="Select a university", value=random_uni[0], style={'width': '90%', 'float': 'right'}),
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'width': '100%', 'marginBottom': '20px', 'padding': '10px', 'boxSizing': 'border-box', 'border': '1px solid #ccc', 'backgroundColor': 'lightgrey'})


