import pandas as pd
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import playercareerstats, teamgamelog
from nba_api.live.nba.endpoints import scoreboard

def get_player_id(name):
    try:
        player = players.find_players_by_full_name(name)
        if player:
            player_id = player[0].get('id', None)
            return player_id
        else:
            return f'Player not found by name: {name}'
    except Exception as e:
        return f'Error: {e}'

def get_team_id(name):
    try:
        team = teams.find_teams_by_full_name(name)
        if team:
            team_id = team[0].get('id', None)
            return team_id
        else:
            return f'Team not found by name: {name}'
    except Exception as e:
        return f'Error: {e}'
    
def get_career(name):
    player_id = get_player_id(name)
    if isinstance(player_id, str):
        return player_id
    try:
        career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
        career_stats_df = career_stats.get_data_frames()[0]

        total_games = career_stats_df['GP'].sum()

        total_points = career_stats_df['PTS'].sum()
        total_rebounds = career_stats_df['REB'].sum()
        total_assists = career_stats_df['AST'].sum()
        field_goals_attempted = career_stats_df['FGA'].sum()
        field_goals_made = career_stats_df['FGM'].sum()

        average_points = round(total_points/total_games, 2)
        average_rebounds = round(total_rebounds/total_games, 2)
        average_assists = round(total_assists/total_games, 2)
        average_field_goal_percentage = round((field_goals_made/field_goals_attempted) * 100, 2)

        return f'{name} averages {average_points} PTS, {average_rebounds} REB, and {average_assists} AST, on {average_field_goal_percentage}% shooting.'

    except Exception as e:
        return f'Error: {e}'

def get_record(name):
    team_id = get_team_id(name)
    if isinstance(team_id, str):
        return team_id
    
    try:
        game_log = teamgamelog.TeamGameLog(team_id=team_id)
        game_log_df = game_log.get_data_frames()[0]

        win_count = game_log_df.iloc[0]['W']
        loss_count = game_log_df.iloc[0]['L']
    
        return f'The {name} are {win_count} - {loss_count}.'
    except Exception as e:
        return f'Error: {e}'

def get_game_score(name):
    team_id = get_team_id(name)
    if isinstance(team_id, str):
        return team_id

    try:
        scoreboard_ = scoreboard.ScoreBoard().get_dict()
        total_games = scoreboard_['scoreboard']['games']

        for game in total_games:
            home_team = game['homeTeam']
            away_team = game['awayTeam']

            if home_team['teamId'] == team_id or away_team['teamId'] == team_id:
               
                home_score = home_team['score']
                away_score = away_team['score']

                home_team_name = f'{home_team['teamCity']} {home_team['teamName']}'
                away_team_name = f'{away_team['teamCity']} {away_team['teamName']}'

                return f'{home_team_name} {home_score} - {away_team_name} {away_score}'
            
        return f'The {name} do not play today.'

    except Exception as e:
        return f'Error: {e}'
