#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def exists(db_cursor, match_table):
    db_cursor.execute(
                "SELECT EXISTS ("
                "SELECT 1 "
                "FROM information_schema.tables "
                "WHERE table_name = %s)", (match_table,)
            )
    if(db_cursor.fetchall()[0][0]):
        return True
    else:
        return False


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    if(exists(c, 'matches')):
        c.execute("DELETE FROM matches")
        DB.commit()
        DB.close()
        return True
    else:
        DB.close()
        return False


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    if(exists(c, 'players')):
        c.execute("DELETE FROM players")
        DB.commit()
        DB.close()
        return True
    else:
        DB.close()
        return False


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    if(exists(c, 'players')):
        c.execute("SELECT count(id) FROM players")
        player_count = c.fetchall()[0][0]
        DB.close()
        return player_count
    else:
        DB.close()
        return 0


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    if(exists(c, 'players')):
        c.execute("INSERT INTO players (name) VALUES (%s)", (name,))
        DB.commit()
        DB.close()
        return True
    else:
        DB.close()
        return False


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    Players are ranked by wins. If multiple players have the same number of
    wins, they are ranked by their opponent match wins (OMW). OMW is the
    total number of match wins that all of their prior opponents have. The
    first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches, omw):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    c = DB.cursor()
    if(exists(c, 'player_details')):
        c.execute(
                "SELECT id, name, wins, matches, omw "
                "FROM player_details "
                "ORDER BY wins DESC, omw DESC"
            )
        standings = c.fetchall()
        DB.close()
        return standings
    else:
        DB.close()
        return False


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    if(exists(c, 'matches')):
        c.execute(
                "INSERT INTO matches (player_id, opponent_id, outcome) "
                "VALUES (%s, %s, %s)", (winner, loser, 'win')
            )
        c.execute(
                "INSERT INTO matches (player_id, opponent_id, outcome) "
                "VALUES (%s, %s, %s)", (loser, winner, 'loss')
            )
        DB.commit()
        DB.close()
    else:
        DB.close()
        return False


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    pair_list = []
    for i in xrange(0, countPlayers() // 2):
        pair_list.append(
            (
                standings[2*i][0],
                standings[2*i][1],
                standings[2*i+1][0],
                standings[2*i+1][1]
            )
        )
    return pair_list
