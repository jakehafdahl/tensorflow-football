import sqlalchemy
from sqlalchemy import String, Integer, ForeignKey, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Position(Base):
    __tablename__ = 'player_positions'
    id = Column(String, primary_key=True)
    abbr = Column(String)


class Player(Base):
    __tablename__ = 'players'
    id = Column(String, primary_key=True)
    last_name = Column(String)
    first_name = Column(String)

    position_id = Column(String, ForeignKey('player_positions.id'))


class Game(Base):
    __tablename__ = 'games'
    id = Column(String, primary_key=True)

    season_id = Column(String, ForeignKey('seasons.id'))
    home_id = Column(String, ForeignKey('game_teams.id'))
    away_id = Column(String, ForeignKey('game_teams.id'))


class GameTeam(Base):
    __tablename__ = 'game_teams'
    id = Column(String, primary_key=True)

    home_game = relationship("Game", foreign_keys = "[Game.home_id]", uselist=False )
    away_game = relationship("Game", foreign_keys = "[Game.away_id]", uselist=False )


class GamePlayer(Base):
    __tablename__ = 'game_players'
    id = Column(String, primary_key=True)

    source_id = Column(String, ForeignKey('players.id'))
    game_team_id = Column(String, ForeignKey('game_teams.id'))
    game_team = relationship("GameTeam")
    pass_statistics = relationship("PassStatistics", back_populates="game_player", uselist=False)


class PassStatistics(Base):
    __tablename__ = 'game_player_pass_statistics'
    id = Column(String, primary_key=True)
    game_player_id = Column(String, ForeignKey('game_players.id'))

    attempts = Column(Integer)
    game_player = relationship(GamePlayer, back_populates="pass_statistics")


def get_all_position_players(position):
    engine = create_engine()
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session();
    return session.query(Player).join(Position).filter(Position.abbr == position.upper()).all()


def get_game_players(player):
    engine = create_engine()
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session();
    return session.query(GamePlayer).join(Player).filter(Player.id == player.id).all()
        

def get_game_season_from_game_player(game_player):
    engine = create_engine()
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session();
    return session.query(Game).join(GameTeam).filter(GameTeam.id == game_player.game_team_id).first()


def create_engine():
    engine = sqlalchemy.create_engine('mysql+mysqldb://root:abc.123@localhost/nfl.premium.dev')
    return engine


def calculate_season_score(game_list, scoring_spec):
    # iterate over each game and 
    points = 0
    for game in game_list:
        # calculate points earned and 
        points + scoring_spec(game)
    # return sum
    return points


def qb_scoring_spec(player):
    return player.pass_statistics.attempts * 20 if player.pass_statistics else 0


def run():
    # get all skill position players (id, full_name, other pertinent info
    rbs = get_all_position_players('qb')
    # for each player get all of the game_players associated to them
    seasons = {}
    for player in rbs:
        # for each game_player get game in order to get the season id
        player.seasons = {}
        player.season_scores = {}
        for game_player in get_game_players(player):
            # build hash of {season_id :[games]} onto the player
            game = game_player.game_team.home_game if game_player.game_team.home_game else game_player.game_team.away_game 
            if game and game.season_id in player.seasons:
                player.seasons[game.season_id] += [game_player]
            else:
                player.seasons[game.season_id] = [game_player]

        # calculate each seasons score
        for season in player.seasons:
            season_score = calculate_season_score(player.seasons[season], qb_scoring_spec)
            player.season_scores[season] = season_score
            # combine players into season hashes with their season score
            seasons[season] = seasons[season] if season in seasons else []
            seasons[season].append({'player': player, 'score': season_score});

        # order by season score and assign them their index 
    for season_key in seasons:
        seasons[season_key].sort(key = lambda entry: entry['score'])
        print "top player for this season is %s" % seasons[season_key][0]
    # save to a pickle to not have to do this again

if __name__ == '__main__':
    run()
