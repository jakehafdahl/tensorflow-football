import MySQLdb

db = MySQLdb.connect(host='localhost', user='root', passwd='abc.123', db='nfl.premium.dev')
cursor = db.cursor()

def get_all_position_players():
    cursor.execute("""SELECT pl.full_name, pos.abbr, pos.desc FROM players as pl
        inner join player_positions as pos on pl.position_id = pos.id
        where pos.abbr in ('QB','RB','WR','TE')""")
    return cursor.fetchall()

def run():
    # get all skill position players (id, full_name, other pertinent info
    raw_players = get_all_position_players()
    # for each player get all of the player_records for them

    # for each player_record get the record_holder, then season associated with them

    # using the season, player_record, and record_holder, get all of the statistics for a given season for that player


if __name__ == '__main__':
    run()
