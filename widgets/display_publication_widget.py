import threading
from queue import Queue
from dash import html, dcc, Input, Output
from adapters.mysql_adapter import MySQLDatabase
import plotly.graph_objs as go
import datetime
import pandas as pd

def build_content(mysql: MySQLDatabase, selected_faculty: str, selected_topic: str) -> html.Div:
    selected_faculty = selected_faculty.replace("'", "\\'")
    # Retrieve information for the selected faculty member
    query = "SELECT f.name, p.title, p.year FROM faculty f \
             JOIN faculty_publication fp ON f.id = fp.faculty_id\
             JOIN publication p ON fp.publication_id = p.id WHERE f.name = '" + selected_faculty + "'"

    result_queue1 = Queue()
    thread1 = threading.Thread(target=mysql.execute_query_async, args=(query, result_queue1))
    thread1.start()
    thread1.join()
    faculty_publications = result_queue1.get()
    df_faculty_publications = pd.DataFrame(faculty_publications, columns=["Faculty", "Publication", "Year"])

    # Retrieve information for the selected topic
    query2 = f"SELECT f.name AS faculty, p.title AS publication, p.year AS year FROM faculty f \
                   JOIN faculty_publication fp ON f.id = fp.faculty_id \
                   JOIN publication p ON fp.publication_id = p.id \
                   JOIN publication_keyword pk ON p.id = pk.publication_id \
                   JOIN keyword k ON pk.keyword_id = k.id \
                   WHERE f.name = '{selected_faculty}' AND k.name = '{selected_topic}' \
                   GROUP BY p.id"

    result_queue2 = Queue()
    thread2 = threading.Thread(target=mysql.execute_query_async, args=(query2, result_queue2))
    thread2.start()
    thread2.join()
    topic_publications = result_queue2.get()
    df_topic_publications = pd.DataFrame(topic_publications, columns=["Faculty", "Publication", "Year"])

    # Create a dictionary to store the number of publications per year for all publications
    publications_per_year_all = {}
    if not df_faculty_publications.empty:
        for _, row in df_faculty_publications.iterrows():
            year = datetime.datetime.strptime(row["Year"], '%Y')
            if year.year in publications_per_year_all:
                publications_per_year_all[year.year] += 1
            else:
                publications_per_year_all[year.year] = 1

    # handle years with zero publications
    if publications_per_year_all:
        min_year = min(publications_per_year_all.keys())
        max_year = max(publications_per_year_all.keys())
        year_range = max_year - min_year + 1

        if year_range < 10:
            # If the range of years with publications is less than 10 years, set the year range to a default value
            min_year = 2000 # max(2000, max_year - 9)
            max_year = 2022

        for year in range(min_year, max_year + 1):
            if year not in publications_per_year_all:
                publications_per_year_all[year] = 0

    else:
        # If there are no publications, set the range of years to a default value of 10 years
        min_year = 2000
        max_year = 2022
        for year in range(min_year, max_year + 1):
            publications_per_year_all[year] = 0

    # Create a dictionary to store the number of publications per year for selected topic
    publications_per_year_topic = {}
    if not df_topic_publications.empty:
        for _, row in df_topic_publications.iterrows():
            year = datetime.datetime.strptime(row["Year"], '%Y')
            if year.year in publications_per_year_topic:
                publications_per_year_topic[year.year] += 1
            else:
                publications_per_year_topic[year.year] = 1

    # Add missing years with zero publications
    if publications_per_year_topic:
        min_year = min(publications_per_year_topic.keys())
        max_year = max(publications_per_year_topic.keys())
        year_range = max_year - min_year + 1

        if year_range < 10:
            # If the range of years with publications is less than 10 years,
            # set the year range to a default value of 10 years
            min_year = 2000 # max(2000, max_year - 9)
            max_year = 2022

        for year in range(min_year, max_year + 1):
            if year not in publications_per_year_topic:
                publications_per_year_topic[year] = 0

    else:
        # If there are no publications, set the range of years to a default value of 10 years
        min_year = 2000
        max_year = 2022
        for year in range(min_year, max_year + 1):
            publications_per_year_topic[year] = 0

    # Create a list of tuples for the number of publications per year for all publications, sorted by year
    publications_list_all = sorted(list(publications_per_year_all.items()))

    # Create a list of tuples for the number of publications per year for the selected topic, sorted by year
    publications_list_topic = sorted(list(publications_per_year_topic.items()))

    # Define the layout of the bar charts
    layout = go.Layout(
        title={'text': f"Publications per Year for {selected_faculty}",
               'x': 0.5, 'font': {'size': 24}},
        xaxis=dict(title='Year', titlefont=dict(size=18), tickfont=dict(size=14)),
        yaxis=dict(title='Number of Publications', titlefont=dict(size=18), tickfont=dict(size=16)),
        barmode='overlay',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        plot_bgcolor='#EAF0E1'
    )

    if len(publications_list_all) >= 1:
        bar_data_all = [go.Bar(
            x=[item[0] for item in publications_list_all],
            y=[item[1] for item in publications_list_all],
            marker=dict(
                color='rgba(76, 181, 245, 0.9)',
                line=dict(
                    color='rgba(76, 181, 245, 0.9)',
                    width=1),
            ),
            opacity=0.9,
            name='Publications per Year (All)'
        )]

        if publications_list_topic:
            bar_data_topic = [go.Bar(
                x=[item[0] for item in publications_list_topic],
                y=[item[1] for item in publications_list_topic],
                marker=dict(
                    color='rgba(238, 105, 63, 1.0)',
                    line=dict(
                        color='rgba(255, 105, 63, 1.0)',
                        width=1),
                ),
                opacity=1.0,
                name='Publications per Year (Topic)'
            )]
            data = bar_data_all + bar_data_topic
        else:
            data = bar_data_all

    # Create the figure
    fig = go.Figure(data=data, layout=layout)

    # Return the plotly graph in a div container
    return html.Div([
        dcc.Graph(figure=fig)
    ])

