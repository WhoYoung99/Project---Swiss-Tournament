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
	ID serial PRIMARY KEY,
	winGame integer,
	totalGame integer
);

CREATE TABLE Matches (
	-- Matches table records all matches' results.
	matchID serial PRIMARY KEY,
	winner integer REFERENCES Players(ID),
	loser integer REFERENCES Players(ID)
);