
import time
import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import flask
from game.game import Game
from widgets import basic_statistics_widget, \
    select_university_widget, \
    faculty_members_list_widget, \
    display_faculty_info_widget, \
    display_publication_widget, \
    score_widget, \
    select_debate_topic_widget
from adapters.mysql_adapter import MySQLDatabase
from adapters.mongo_adapter import MongoDatabase
from widgets.debate_results_modal import getModal

# initialize app
app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP, 'assets/style.css'], 
           suppress_callback_exceptions=True, 
           title="Academic World",
           update_title="Loading...", 
           prevent_initial_callbacks='initial_duplicate')

application = app.server

PlayRound = {
    'university0': None,  # University 1
    'university0_photo': None,  # University 1 photo
    'university1': None,  # University 2
    'university1_photo': None,  # University 2 photo
    'player0': None,  # Player 1
    'player1': None,  # Player 2
    'topic': None,  # Topic
    'score0': 0,  # Score 1
    'score1': 0,  # Score 2
}

# Connect to MySQL
mysql = MySQLDatabase()
mysql.connect()

# Connect to MongoDB
mongo = MongoDatabase()
mongo.connect()

widgetContainerStyle = {'width': 'calc(33.33% - 10px)', 'marginBottom': '20px', 'padding': '10px',
                        'boxSizing': 'border-box', 'border': '1px solid #ccc'}

app.layout = html.Div(children=[

    # Header widget
    html.Div([
        html.Div(style={'width': '10%', 'opacity': '0'}),
        html.Div(["Faculty debates"], style={'width': '80%', 'textAlign': 'center', 'fontSize': '30px', "flex": "1"}),
        html.Div(basic_statistics_widget.build_content(mysql),
                 style={'width': '10%', 'float': 'right', 'fontSize': '12px'})
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'width': '100%',
              'marginBottom': '20px', 'padding': '10px', 'boxSizing': 'border-box', 'border': '1px solid #ccc',
              'backgroundColor': 'lightgreen'}),

    # Select university widgets
    html.Div([
        html.Div(select_university_widget.build_content(mysql, 0), style={'width': '45%', 'display': 'inline-block',
                                                                          'float': 'left'}),
        html.Div(score_widget.build_content(0, 0), id='score_board', style={'width': '10%', 'display': 'inline-block',
                                                                            'float': 'left'}),
        html.Div(select_university_widget.build_content(mysql, 1), style={'width': '45%', 'display': 'inline-block',
                                                                          'float': 'right'}),
    ], style={'textAlign': 'center', 'marginTop': '20px'}),

    # start debate button
    html.Div([
        html.Button('Start debate', id='start_debate_button', disabled=True, n_clicks=0,
                    style={'width': '95%', 'height': '70px', 'fontSize': '20px', 'backgroundColor': 'orange',
                           'cursor': 'pointer'})
    ], style={'textAlign': 'center', 'marginTop': '20px'}),

    # Select Debate topic widget
    html.Div([
        html.Div(select_debate_topic_widget.build_content(mysql),
                 style={'width': '100%', 'display': 'inline-block', 'float': 'left'}),
    ], style={'textAlign': 'center', 'marginTop': '20px'}),

    # Display Faculty members
    html.Div([
        html.Div(faculty_members_list_widget.build_content(mysql, "", 0), id='list_faculty_members0', style={'width': '50%', 'display': 'inline-block'}),
        html.Div(faculty_members_list_widget.build_content(mysql, "", 1), id='list_faculty_members1', style={'width': '50%', 'display': 'inline-block'}),
    ], style={}),

    # Display Faculty info
    html.Div([
        html.Div(display_faculty_info_widget.build_content(mongo, "", 0), id='display_faculty_info0',
                 className="faculty-info-container", style={'width': '50%', 'display': 'inline-block', 'height': '200px'}),
        html.Div(display_faculty_info_widget.build_content(mongo, "", 1), id='display_faculty_info1',
                 className="faculty-info-container", style={'width': '50%', 'display': 'inline-block', 'height': '200px'}),
    ], style={'border': '2px solid blue', 'padding': '20px'}),

    # Display Publication info
    html.Div([
        html.Div(display_publication_widget.build_content(mysql, "", ""), id='display_publication0',
                 className="publication-container",
                 style={'width': '50%', 'display': 'inline-block', 'float': 'left'}),
        html.Div(display_publication_widget.build_content(mysql, "", ""), id='display_publication1',
                 className="publication-container",
                 style={'width': '50%', 'display': 'inline-block', 'float': 'right'}),
    ], style={'textAlign': 'center', 'marginTop': '20px', 'height': '470px', 'border': '2px solid green',
              'padding': '10px'}),

    getModal(mysql),
    dcc.Loading(id="loading", children=[], type="default", fullscreen=True)
])


####################
# Callbacks
# Don't like the idea to have callbacks here and not in the widget files, but it should have access to
# `app` which is available only in main file. If I'll import `app` in widgets files, it will be circular
# dependency because this file imports widgets.
####################
# Start Debate button click handler
@app.callback(
    [dash.dependencies.Output('loading', 'children'),
     dash.dependencies.Output('modal', 'is_open'),
     dash.dependencies.Output('univer_winner', 'children'),
     dash.dependencies.Output('univer_winner_logo', 'src'),
     dash.dependencies.Output('player_winner', 'children'),
     dash.dependencies.Output('faculty_interest_explanation', 'children'),
     dash.dependencies.Output('faculty_publications_explanation', 'children'),
     dash.dependencies.Output('score_board', 'children', allow_duplicate=True)],
    [dash.dependencies.Input('start_debate_button', 'n_clicks')],
    [dash.dependencies.State('modal', 'is_open')]
    )
def start_debate(n_clicks, is_open):
    if n_clicks:
        print(f"Start debate button clicked. n_clicks: {n_clicks}, is_open: {is_open}")
        game = Game(mysql, PlayRound['university0'], PlayRound['university1'])
        print(f"Game initialized with university0: {PlayRound['university0']}, university1: {PlayRound['university1']}")
        
        game.start_debate(PlayRound['player0'], PlayRound['player1'], PlayRound['topic'])
        time.sleep(1.5)
        univer, player = game.get_winner()
        print(f"Debate results - winner university: {univer}, winner player: {player}")

        if univer == PlayRound['university0']:
            PlayRound['score0'] += 1
        elif univer == PlayRound['university1']:
            PlayRound['score1'] += 1

        mysql.update_score(PlayRound['university0'], PlayRound['score0'], PlayRound['university1'], PlayRound['score1'],
                           PlayRound['topic'])
        print(f"Updated scores - university0: {PlayRound['score0']}, university1: {PlayRound['score1']}")
        
        return [], not is_open, \
            univer, \
            PlayRound['university0_photo'] if univer == PlayRound['university0'] else PlayRound['university1_photo'], \
            player, \
            game.explanation['interest'], \
            game.explanation['publications'], \
            score_widget.build_content(PlayRound['score0'], PlayRound['score1'])
    else:
        return [], is_open, "", "", "", "", "", score_widget.build_content(PlayRound['score0'], PlayRound['score1'])


# Close modal window
@app.callback(
    [dash.dependencies.Output('modal', 'is_open', allow_duplicate=True),
     dash.dependencies.Output('list_faculty_members0', 'children', allow_duplicate=True),
     dash.dependencies.Output('list_faculty_members1', 'children', allow_duplicate=True)],
    [dash.dependencies.Input("close_modal", "n_clicks")],
    [dash.dependencies.State('modal', 'is_open')])
def close_modal(n_clicks, is_open):
    if not n_clicks:
        return dash.no_update, dash.no_update, dash.no_update
    return not is_open, \
        faculty_members_list_widget.build_content(mysql, PlayRound['university0'], 0), \
        faculty_members_list_widget.build_content(mysql, PlayRound['university1'], 1)


# Select university dropdown handler
@app.callback(
    [dash.dependencies.Output('score_board', 'children'),
     dash.dependencies.Output('start_debate_button', 'disabled')],
    [dash.dependencies.Input('select_university_dropdown0', 'value'),
     dash.dependencies.Input('select_university_dropdown1', 'value'),
     dash.dependencies.Input('select_debate_topic_dropdown', 'value')])
def update_score_board(uni_name_0, uni_name_1, topic):
    PlayRound['university0'] = uni_name_0
    PlayRound['university1'] = uni_name_1
    PlayRound['topic'] = topic
    min_uni, max_uni = sorted([uni_name_0, uni_name_1])
    result = mysql.execute_query(
        f"select score1, score2 from scores where university1 = '{min_uni}' and university2 = '{max_uni}' and topic = '{topic}'")
    if len(result) == 0:
        PlayRound['score0'] = 0
        PlayRound['score1'] = 0
        mysql.set_initial_score(min_uni, max_uni, topic)
        return score_widget.build_content(0, 0), False
    if uni_name_0 < uni_name_1:
        PlayRound['score0'] = result[0][0]
        PlayRound['score1'] = result[0][1]
        return score_widget.build_content(result[0][0], result[0][1]), False
    else:
        PlayRound['score0'] = result[0][1]
        PlayRound['score1'] = result[0][0]
        return score_widget.build_content(result[0][1], result[0][0]), False


@app.callback(
    [dash.dependencies.Output('list_faculty_members0', 'children'),
     dash.dependencies.Output('university_image0', 'src')],
    [dash.dependencies.Input('select_university_dropdown0', 'value')])
def university_0_selection(value):
    if value is None:
        return [], ""
    stripped_value = value.replace('\'', '\\\'')
    result = mysql.execute_query(f"SELECT photo_url FROM university WHERE name = '{stripped_value}'")
    PlayRound['university0_photo'] = result[0][0] if len(result) > 0 else ""
    return faculty_members_list_widget.build_content(mysql, value, 0), \
        result[0][0] if len(result) > 0 else ""


@app.callback(
    [dash.dependencies.Output('list_faculty_members1', 'children'),
     dash.dependencies.Output('university_image1', 'src')],
    [dash.dependencies.Input('select_university_dropdown1', 'value')])
def university_1_selection(value):
    if value is None:
        return [], ""
    stripped_value = value.replace('\'', '\\\'')
    result = mysql.execute_query(f"SELECT photo_url FROM university WHERE name = '{stripped_value}'")
    PlayRound['university1_photo'] = result[0][0] if len(result) > 0 else ""
    return faculty_members_list_widget.build_content(mysql, value, 1), \
        result[0][0] if len(result) > 0 else ""


@app.callback(
    [dash.dependencies.Output('display_faculty_info0', 'children'),
     dash.dependencies.Output('display_publication0', 'children')],
    [dash.dependencies.Input('university_members_table_0', 'selected_cells'),
     dash.dependencies.Input('select_debate_topic_dropdown', 'value')],
    [dash.dependencies.State('university_members_table_0', 'data')])
def display_faculty_info0(active_cell, topic, data):
    try:
        if len(active_cell) > 0 and len(data) > 0:
            name = data[active_cell[0]['row']]['Name']
            PlayRound['player0'] = name
            return display_faculty_info_widget.build_content(mongo, name, 0), \
                display_publication_widget.build_content(mysql, name, topic)
        else:
            return display_faculty_info_widget.build_content(mongo, "", 0), \
                display_publication_widget.build_content(mysql, "", "")
    except Exception as e:
        print(e)
        return ("", "")


@app.callback(
    [dash.dependencies.Output('display_faculty_info1', 'children'),
     dash.dependencies.Output('display_publication1', 'children')],
    [dash.dependencies.Input('university_members_table_1', 'selected_cells'),
     dash.dependencies.Input('select_debate_topic_dropdown', 'value')],
    [dash.dependencies.State('university_members_table_1', 'data')])
def display_faculty_info1(active_cell, topic, data):
    if len(active_cell) > 0 and len(data) > 0:
        name = data[active_cell[0]['row']]['Name']
        PlayRound['player1'] = name
        return display_faculty_info_widget.build_content(mongo, name, 1), \
            display_publication_widget.build_content(mysql, name, topic)
    else:
        return display_faculty_info_widget.build_content(mongo, "", 1), \
            display_publication_widget.build_content(mysql, "", "")


if __name__ == '__main__':
    application.run( host= '0.0.0.0', port='8080')
