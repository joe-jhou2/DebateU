from adapters.mysql_adapter import MySQLDatabase

class Game:
    def __init__(self, mysql: MySQLDatabase, university_1: str, university_2: str):
        self.player2 = None
        self.player1 = None
        self.id = "-".join(sorted([university_1, university_2]))
        self.mysql = mysql
        self.university_1 = university_1
        self.university_2 = university_2
        self.player_1_score = 0
        self.player_2_score = 0
        self.explanation = {}


    def start_debate(self, player1: str, player2: str, topic: str):
        self.player1 = player1
        self.player2 = player2

        # Calculate interest score based on faculty's interest
        self.player_1_score = (50 * self.get_player_interest_score(player1, topic))
        self.player_2_score = (50 * self.get_player_interest_score(player2, topic))
        print(f"Interest scores: {player1}={self.player_1_score}, {player2}={self.player_2_score}")
        
        # Calculate score based on faculty's publications on the topic
        player1_pub_score = sum(self.get_publications_score(player1, topic))
        player2_pub_score = sum(self.get_publications_score(player2, topic))
        print(f"Publication scores: {player1}={player1_pub_score}, {player2}={player2_pub_score}")

        self.explanation["interest"] = f"{player1} got {self.player_1_score} points, {player2} got {self.player_2_score} points for their interest in {topic}"
        self.explanation["publications"] = f"{player1} got {player1_pub_score} points, {player2} got {player2_pub_score} points for their publications on topic {topic}"

        self.player_1_score += (player1_pub_score)
        self.player_2_score += (player2_pub_score)
        print(f"Total scores: {player1}={self.player_1_score}, {player2}={self.player_2_score}")


    def get_player_interest_score(self, player: str, topic: str):
        # Get faculty interest
        result = self.mysql.execute_query(f"select fk.score from faculty as f, faculty_keyword as fk, keyword as k where f.id = fk.faculty_id and f.name = '{player}' and fk.keyword_id = k.id and k.name = '{topic}'")
        print(f"Interest score query result for {player}: {result}")
        if len(result) == 0:
            return 0
        return result[0][0]
    

    def get_publications_score(self, faculty: str, keyword: str) -> list:
        # Create the query string with embedded parameters
        query = f"""
            SELECT p.num_citations * pk.score
            FROM faculty f
            JOIN faculty_publication fp ON f.id = fp.faculty_id
            JOIN publication p ON fp.publication_id = p.id
            JOIN publication_keyword pk ON p.id = pk.publication_id
            JOIN keyword k ON pk.keyword_id = k.id
            WHERE f.name = %s AND k.name = %s
        """
        result = self.mysql.execute_query(query, (faculty, keyword))
        print(f"Publication score query result for {faculty}: {result}")
        if result is None:
            return []
        return [row[0] for row in result]

    def get_winner(self):
        print(f"Scores: {self.player1}={self.player_1_score}, {self.player2}={self.player_2_score}")
        if self.player_1_score > self.player_2_score:
            return self.university_1, self.player1
        elif self.player_1_score < self.player_2_score:
            return self.university_2, self.player2
        else:
            return "Draw", "Draw"


