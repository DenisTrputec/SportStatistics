import sqlite3


class Database:
    def __init__(self, db_path="temp.db"):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def __get_teams(self):
        self.cursor.execute("SELECT * FROM team")
        return self.cursor.fetchall()

    def insert_matches(self, matches, match_type_id, is_test=False):
        teams = self.__get_teams()
        values = []
        for match in matches:
            home_team_id = away_team_id = None
            for team in teams:
                if match["home_team_name"] == team[1]:
                    home_team_id = team[0]
                elif match["away_team_name"] == team[1]:
                    away_team_id = team[0]
                if home_team_id and away_team_id:
                    break
            values.append((home_team_id, away_team_id, match["home_goals"], match["away_goals"], match_type_id,
                           match["date"], match["stadium"], match["attendance"], match["referee"]))

        for v in values:
            print(v)
        if not is_test:
            columns = "home_team_id, away_team_id, home_goals, away_goals, " \
                      "match_type_id, date, stadium, attendance, referee"
            self.cursor.executemany(f'INSERT INTO match ({columns}) '
                                    f'VALUES (?,?,?,?,?,?,?,?,?);', values)
            self.connection.commit()
