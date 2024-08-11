# This widget displays basic information for the selected faculty member
import threading
from queue import Queue
import time
from dash import html
from adapters.mongo_adapter import MongoDatabase
from scholarly import scholarly


def build_content(mongo: MongoDatabase, selected_faculty: str, player: int) -> html.Div:
    # Initialize variables
    # author_url = None
    # scholar_id = None
    
    # Retrieve information for the selected faculty member
    # query = {'name': selected_faculty}
    # faculty_info = mongo.execute_query('faculty', query)
    query = {'name': selected_faculty}
    result_queue = Queue()
    thread = threading.Thread(target=mongo.execute_query_async, args=('faculty', query, result_queue))
    thread.start()
    thread.join()
    faculty_info = result_queue.get()

    # If no results were returned, set default values
    if not faculty_info:
        faculty_info = [
            {"name": "Not available", "position": "Not available",
             "affiliation": {"name": "Not available"}, "email": "Not available",
             "researchInterest": "Not available",
             "phone": "Not available"}]
    else:
        for key in faculty_info[0].keys():
            if not faculty_info[0][key]:
                faculty_info[0][key] = "Not available"

    # if 'author_url' in faculty_info[0] and faculty_info[0]['author_url'] is not None:
    #     author_url = faculty_info[0]['author_url']
    # else:
    #     if faculty_info[0]['name'] != "Not available":
    #         author_url, scholar_id = None, None
    #         retries = 3
    #         delay = 2  # Start with a 2-second delay
    #         while retries > 0:
    #             try:
    #                 if faculty_info[0]['email'] is not None and "@" in faculty_info[0]['email']:
    #                     email_domain = faculty_info[0]['email'].split('@')[1]
    #                     search_query = scholarly.search_author(f"{faculty_info[0]['name']}, {email_domain}")
    #                 else:
    #                     search_query = scholarly.search_author(faculty_info[0]['name'])

    #                 author = next(search_query)
    #                 scholar_id = author['scholar_id']
    #                 author_url = f"https://scholar.google.com/citations?user={scholar_id}&hl=en"
    #                 break  # Exit the loop if successful

    #             except StopIteration:
    #                 # Handle the case where the search query returned no results
    #                 author_url = None
    #                 scholar_id = None
    #                 break  # No point in retrying if the search failed

    #             except Exception as e:
    #                 # Handle any other exceptions (network issues, rate limiting, etc.)
    #                 retries -= 1
    #                 if retries > 0:
    #                     time.sleep(delay)
    #                     delay *= 2  # Exponential backoff
    #                 else:
    #                     # If retries are exhausted, log the error and set default values
    #                     print(f"Error querying Google Scholar: {e}")
    #                     author_url = None
    #                     scholar_id = None

    #     # Store the scholar_id and author_url in MongoDB for future use
    #     if author_url:
    #         mongo.update_document('faculty', {'name': selected_faculty},
    #                               {'$set': {'scholar_id': scholar_id, 'author_url': author_url}})

    # Create the layout for the widget using HTML and CSS
    content = html.Div([
        html.H2(faculty_info[0]['name'], id=f"faculty_name_{player}", className="faculty-name", style={'text-align': 'center'}),
        html.P(faculty_info[0]['position'], className="faculty-position"),
        html.P(["Affiliation: ", html.Span(faculty_info[0]['affiliation']['name'], style={'font-style': 'italic'})],
               className="faculty-affiliation"),
        html.P(["Email: ", html.Span(faculty_info[0]['email'], style={'color': 'blue'})],
               className="faculty-email"),
        html.P(f"Research Interests:  {faculty_info[0]['researchInterest']}", className="faculty-interests"),
        html.P(f"Phone: {faculty_info[0]['phone']}", className="faculty-phone")
        # html.P(html.A('Google Scholar Page', href=author_url, target="_blank")) if author_url else html.P("Google Scholar Page: Not available"),
    ], className="faculty-info-widget",
        style={'textAlign': 'left', 'width': '100%', 'height': '100%', 'padding': '10px', 'backgroundColor': 'white'})

    return content


