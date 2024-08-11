# DebateU: Academic Faculty Debate Simulator
# Link: http://54.193.249.61:8080

DebateU is an interactive web application designed to simulate academic debates between faculty members from different universities. 
The application randomly selects faculty members to compete on various research topics, 
providing users with both entertainment and insights into academic strengths across universities.

## Authorship
Joe Hou and Tsekinovsky Boris designed and developed this application in April 2023. Joe Hou later updated the code and managed its deployment.

## Usage

1. **Select University Teams**: Start by choosing university teams from a dropdown menu containing available universities in the dataset. Each player selects their university team separately.

2. **Choose Debate Topic**: Enter keywords related to the topic of debate in the "Select a topic for discussion" box. The application suggests related keywords as you type.

3. **Select Faculty Members**: A list of faculty members from the selected universities is displayed. Choose one faculty member per round of debate by clicking on their name.

4. **Initiate Debate**: Click the "Debate" button to start the debate. The game consists of 10 rounds, with each round awarding points to the winning team based on faculty members' arguments and expertise.

5. **View Results**: Faculty members' basic information, including their name, affiliation, and research interests, is displayed. Publications related to the selected topic are highlighted. Additionally, the shortest paths connecting faculty members to the chosen topic are visualized.

## Implementation

- **Framework**: Built using the Dash framework, DebateU provides an intuitive user interface with interactive components.
  
- **Data Management**: Utilizes MySQL, MongoDB databases to store and retrieve game-related data, faculty information, and scholarly publications.
  
- **External Data Integration**: Integrates with the Google Scholar API to retrieve and display additional information about faculty members and their publications.

- **Performance Optimization**: Implements asynchronous data retrieval using a queue-based approach to enhance application responsiveness.
