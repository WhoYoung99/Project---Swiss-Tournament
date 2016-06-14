-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament
-- Enter tournament database

CREATE TABLE Players (
	-- Players table records each player's basic info.
	Name text,
	ID serial PRIMARY KEY
);

CREATE TABLE Matches (
	-- Matches table records all matches' results.
	matchID serial PRIMARY KEY,
	winner integer REFERENCES Players(ID),
	loser integer REFERENCES Players(ID)
);

-- create win recording view, count the number of wins by player.
CREATE VIEW wincounter
AS
	SELECT Players.Name, Players.ID, COUNT(Matches.winner) as wins
	FROM Players LEFT JOIN Matches
		ON Players.ID = Matches.winner
	GROUP BY Players.ID;

-- create total game view, count the total number of games by player.
CREATE VIEW gamecounter
AS
	SELECT Players.Name, Players.ID, COUNT(Matches) as total
	FROM Players LEFT JOIN Matches
		ON Players.ID = Matches.winner or Players.ID = Matches.loser
	GROUP BY Players.ID;

-- create standing view, for 'playerStandings()' usage.
CREATE VIEW standing
AS
	SELECT wincounter.Name,  wincounter.ID, wincounter.wins, gamecounter.total
	FROM wincounter, gamecounter
	WHERE wincounter.ID = gamecounter.ID
	ORDER BY wins DESC;