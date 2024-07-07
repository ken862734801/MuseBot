import pandas as pd
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import teamgamelog

def get_player_id(name):
    try:
        player = players.find_players_by_first_name(name)
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
    