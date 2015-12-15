""" Models for the datas """
import datetime

class Player:

    def __init__(self, row):
        """
                ID, last name, first name, position, birth year, debut year
        """
        self._id = row[0]
        self._lastname = row[1]
        self._firstname = row[2]
        self._position = row[3]
        self._birthyear = int(row[4])
        self._rookieyear = int(row[5])
        self._seasons = []
    
    
    def id(self):
        return self._id
    
    def name(self):
        return self._firstname + ' ' + self._lastname

    def position(self):
        return self._position

    def birthyear(self):
        return self._birthyear

    def age(self):
        return datetime.datetime.now().year - self._birthyear

    def rookieyear(self):
        return self._rookieyear

    def seasons(self, startyear=0):
        return [season for season in self._seasons if season.year() >= startyear]

    def add_season(self, season):
        self._seasons.append(season)


class Season:

    def __init__(self, row):
        """
            ID, last name, first name, year, team, position, G, GS, COMP, ATT, PassYD,
            PassTD, INT, rush, rushYD, rushTD, rec, recYD, recTD
        """
        if row[6] == '':
            row[6] = '0'
        
        if row[7] == '':
            row[7] = '0'
        
        self._id = row[0]
        self._lastname = row[1]
        self._firstname = row[2]
        self._year = int(row[3])
        self._team = row[4]
        self._position = row[5]
        self._gamesplayed = int(row[6])
        self._gamesstarted = int(row[7])
        self._passescompleted = int(row[8])
        self._passesattempted = int(row[9])
        self._passyards = int(row[10])
        self._passtouchdowns = int(row[11])
        self._passinterceptions = int(row[12])
        self._rushattempts = int(row[13])
        self._rushyards = int(row[14])
        self._rushtouchdowns = int(row[15])
        self._receptions = int(row[16])
        self._receptionyards = int(row[17])
        self._receptiontouchdowns = int(row[18])
        self._games = []

    def id(self):
        return self._id

    def year(self):
        return self._year

    def add_game(self, game):
        self._games.append(game)

    def format_data(self):
        return [self._passesattempted, self._passescompleted, self._passtouchdowns, self._passyards, self._passinterceptions, self._rushattempts, self._rushattempts, self._rushtouchdowns, self._receptions, self._receptionyards, self._receptiontouchdowns]


class Game:

    def __init__(self, row):
        """
        ID, year, team, week, opp, comp, att, passYD, PassTD, INT, rush, rushYD,
        rec, recYD, Total TDs rushing and receiving
        """
        if row[6] == '':
            row[6] = '0'
        if row[7] == '':
            row[7] = '0'
        if row[8] == '':
            row[8] = '0'
        if row[9] == '':
            row[9] = '0'
        if row[10] == '':
            row[10] = '0'
        if row[11] == '':
            row[11] = '0'
        if row[12] == '':
            row[12] = '0'
        
        self._id = row[0]
        self._year = int(row[1])
        self._team = row[2]
        self._week = int(row[3])
        self._opponent = row[4]
        self._passescompleted = int(row[5])
        self._passesattempted = int(row[6])
        self._passyards = int(row[7])
        self._passtouchdowns = int(row[8])
        self._passinterceptions = int(row[9])
        self._rushattempts = int(row[10])
        self._rushyards = int(row[11])
        self._receptions = int(row[12])
        self._receptionyards = int(row[13])
        self._totaltouchdowns = int(row[14])


    def id(self):
        return self._id

    def year(self):
        return self._year

    def dump_game_stats(self):
        return [self._passescompleted,
                self._passesattempted]
