import random
import threading
from queue import Queue
from dash import html, dash_table
import dash_bootstrap_components as dbc
from dash.development.base_component import Component
import pandas as pd
from adapters.mysql_adapter import MySQLDatabase


def build_content(mysql: MySQLDatabase, uni: str, player: int) -> Component:

    result_queue = Queue()
    thread = threading.Thread(target=mysql.execute_query_async, args=("select f.name, f.position from faculty as f, university as u where f.university_id = u.id and u.name = '"+ uni +"'", result_queue))
    thread.start()
    thread.join()
    members = result_queue.get()

    df = pd.DataFrame(members, columns=["Name", "Position"])

    random_faculty = random.randint(0, len(members))

    return html.Div([
        dash_table.DataTable(
            id='university_members_table_' + str(player),
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            selected_cells=[{ 'row': random_faculty, 'column': 0}],
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold',
            },
            style_data_conditional=[{
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }],
            style_table={
                'maxHeight': '300px',
                'overflowY': 'scroll',
                'overflowX': 'scroll',
            },
            style_cell={
                'font-family': 'Arial, sans-serif',
                'font-size': '18px',
                'font-weight': 'normal',
                'textAlign': 'left',
            }
        )

    ])


