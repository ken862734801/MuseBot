from nba_api.stats.static import players, teams

class Stat:

    @staticmethod
    def get_player_id(name):
        try:
            player = players.find_players_by_full_name(name)
            if player:
                player_id = player[0].get('id', None)
                return player_id
            else:
                return f'Player not found by name: {name}'
        except Exception as e:
            print(f'Error: {e}')
    
    @staticmethod
    def get_team_id(name):
        try:
            team = teams.find_teams_by_full_name(name)
            print(team)
            if team:
                team_id = team[0].get('id', None)
                return team_id
            else:
                return f'Team not found by name: {name}'
        except Exception as e:
            print(f'Error: {e}')
 