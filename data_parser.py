import csv
from football_classes import Player, Season, Game

def get_master_player_list():
    players = {};
    with open('master.csv', 'rb') as csvfile:
        playerreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in playerreader:
            players[row[0]] = Player(row)

    return players


def get_player_seasons_list():
    seasons = [];
    with open('seasons.csv', 'rb') as csvfile:
        seasonreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in seasonreader:
            seasons.append(Season(row))

    return seasons

def get_player_games_list():
    games = [];
    with open('games.csv', 'rb') as csvfile:
        gamesreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in gamesreader:
            games.append(Game(row))

    return games


def combine_players_seasons_games_lists(players, seasons, games):
    """  """
    # only add seasons for players we know about
    for season in [valid_season for valid_season in seasons if players.has_key(valid_season.id())]:
        players[season.id()].add_season(season)

    # only add games for players we know about
    for game in [valid_game for valid_game in games if players.has_key(valid_game.id())]:
        try:
            season = next(season for season in players[game.id()].seasons() if season.year() == game.year())
            season.add_game(game)
        except StopIteration:
            pass
            #print("There are no seasons for %s" % players[game.id()].name())

    return players


def run():
    players = get_master_player_list()
    seasons = get_player_seasons_list()
    games = get_player_games_list()
    built = combine_players_seasons_games_lists(players, seasons, games)


if __name__ == '__main__':
    run()
