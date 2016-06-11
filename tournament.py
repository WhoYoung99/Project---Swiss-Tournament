#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name = "tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection.
    """
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = conn.cursor()
        return db, cursor
    except:
        print("Database not exists.")


def deleteMatches():
    """Remove all the match records from the database."""
    conn, c = connect()
    c.execute("DROP TABLE matchTable CASCADE;") # need to add CASCADE at the end of DROP caluse
    c.execute("CREATE TABLE matchTable (Name text, ID serial references playerInfo, winGame int, totalGame int);")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn, c = connect()
    c.execute("DROP TABLE playerInfo CASCADE;") # need to add CASCADE at the end of DROP caluse
    c.execute("CREATE TABLE playerInfo (Name text, ID serial primary key);")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn, c = connect()
    QUERY = "SELECT count(*) as num FROM playerInfo"
    c.execute(QUERY)
    return c.fetchall()[0][0]
    conn.close()


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    QUERY = "INSERT INTO playerInfo VALUES (%s)"
    INPUT = name
    conn, c = connect()
    c.execute(QUERY, (INPUT,))
    QUERY = "INSERT INTO matchTable VALUES ( (%s), (SELECT playerInfo.ID FROM playerInfo where playerInfo.Name = (%s)), 0, 0)"
    c.execute(QUERY, (INPUT,INPUT,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn, c = connect()
    QUERY1 = "SELECT playerInfo.ID, playerInfo.Name, matchTable.winGame, matchTable.totalGame "
    QUERY2 = "FROM playerInfo LEFT JOIN matchTable ON playerInfo.ID = matchTable.ID ORDER BY matchTable.winGame DESC"
    c.execute( QUERY1 + QUERY2)
    return c.fetchall()
    conn.close()


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn, c = connect()
    QUERY_win = "UPDATE matchTable SET  winGame = winGame + 1, totalGame = totalGame + 1 where matchTable.ID = (%s)"
    QUERY_los = "UPDATE matchTable SET  totalGame = totalGame + 1 where matchTable.ID = (%s)"
    winID = winner
    losID = loser
    c.execute(QUERY_win, (winID,))
    c.execute(QUERY_los, (losID,))
    conn.commit()
    conn.close()


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
    matchOrder = playerStandings()
    matchList = []
    for i in range(0, len(matchOrder), 2):
        pairing = (matchOrder[i][0], matchOrder[i][1], matchOrder[i+1][0], matchOrder[i+1][1])
        matchList.append(pairing)
    return matchList




