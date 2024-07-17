import pandas as pd
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import playercareerstats, teamgamelog
from nba_api.live.nba.endpoints import boxscore, scoreboard

def get_player_id(name):
    """
    Retrieves the player ID given a player's full name.

    Parameters:
    name (str): Full name of the player.

    Returns:
    int or str: Player ID if found, otherwise an error message or a message indicating the player was not found.
    """
    try:
        player = players.find_players_by_full_name(name)
        print(player)
        if player:
            player_id = player[0].get('id', None)
            return player_id
        else:
            return f'Player not found by name: {name}'
    except Exception as e:
        return f'Error: {e}'

def get_team_id(name):
    """
    Retrieves the team ID given a team's full name.

    Parameters:
    name (str): Full name of the team.

    Returns:
    int or str: Team ID if found, otherwise an error message or a message indicating the team was not found.
    """
    try:
        team = teams.find_teams_by_full_name(name)
        if team:
            team_id = team[0].get('id', None)
            return team_id
        else:
            return f'Team not found by name: {name}'
    except Exception as e:
        return f'Error: {e}'
    
def get_current_team(player_id):
    """
    Retrieves the current team ID of a player given their player ID.

    Parameters:
    player_id (int): Player ID.

    Returns:
    int or str: Current team ID if found, otherwise an error message.
    """
    try:
        career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
        career_stats_df = career_stats.get_data_frames()[0]
        team_id = career_stats_df.iloc[-1]['TEAM_ID']
        return team_id
    except Exception as e:
        return f'Error: {e}'

def get_current_game(player_id):
    """
    Retrieves the current game ID for a player's team given the player's ID.

    Parameters:
    player_id (int): Player ID.

    Returns:
    str: Game ID if a game is found, otherwise a message indicating no game is found or an error message.
    """
    try:
        current_team = get_current_team(player_id)
        if isinstance(current_team, str):
            return current_team
        scoreboard_ = scoreboard.ScoreBoard().get_dict()
        games = scoreboard_['scoreboard']['games']

        for game in games:
            home_team = game['homeTeam']
            away_team = game['awayTeam']

            if home_team['teamId'] == current_team or away_team['teamId'] == current_team:
                return game['gameId']
            
        return 'No game found for the player\'s team today.'
    except Exception as e:
        return f'Error: {e}'

def get_career(name):
    """
    Retrieves the career statistics of a player given their full name.

    Parameters:
    name (str): Full name of the player.

    Returns:
    str: A summary of the player's career statistics, otherwise an error message.
    """
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
    """
    Retrieves the current win-loss record of a team given the team's full name.

    Parameters:
    name (str): Full name of the team.

    Returns:
    str: A summary of the team's current win-loss record, otherwise an error message.
    """
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
    """
    Retrieves the current game score for a team given the team's full name.

    Parameters:
    name (str): Full name of the team.

    Returns:
    str: The current game score if the team is playing, otherwise a message indicating no game is found or an error message.
    """
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
    
def get_boxscore(name):
    """
    Retrieves the box score statistics for a player given the player's full name.

    Parameters:
    name (str): Full name of the player.

    Returns:
    str: A summary of the player's box score statistics, otherwise a message indicating the player does not play today or an error message.
    """
    player_id = get_player_id(name)
    if isinstance(player_id, str):
        return player_id
    
    game_id = get_current_game(player_id)
    if isinstance(game_id, str):
        return game_id
    
    try:
       boxscore_ = boxscore.BoxScore(game_id=game_id).get_dict()
       players = boxscore_['game']['homeTeam']['players'] + boxscore_['game']['awayTeam']['players']

       for player in players:
           if player['personId'] == player_id:
               player_stats = player['statistics']
               points = player_stats['points']
               assists = player_stats['assists']
               rebounds = player_stats['reboundsTotal']
               field_goal_percentage = player_stats['fieldGoalsPercentage'] * 100

               return f'{name} has {points} PTS, {assists} AST, {rebounds} REB, on {field_goal_percentage}% shooting.'
       return 'f{name} does not play today.'
    except Exception as e:
        return f'Error: {e}'
