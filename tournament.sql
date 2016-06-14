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

-- create game recording view, count the number of wins by player.
CREATE VIEW ShowRecords
AS
	SELECT Players.Name, Players.ID, COUNT(Matches) as win_game
	FROM Players LEFT JOIN Matches
		ON Players.ID = Matches.winner
	GROUP BY Players.ID;