from dash import html
from adapters.mysql_adapter import MySQLDatabase

def build_content(mysql: MySQLDatabase):

    professors = mysql.execute_query("select count(*) from faculty")
    universities = mysql.execute_query("select count(*) from university")
    keywords = mysql.execute_query("select count(*) from keyword")

    return html.Table([
        html.Tbody([
            html.Tr([
                html.Td("Faculty members"),
                html.Td(professors[0])
            ]),
            html.Tr([
                html.Td("Universities"),
                html.Td(universities[0])
            ]),
            html.Tr([
                html.Td("Keywords/Topics"),
                html.Td(keywords[0])
            ])
        ])
    ])
