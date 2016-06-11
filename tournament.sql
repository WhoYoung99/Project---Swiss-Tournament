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

CREATE TABLE playerInfo (
	Name text,
	ID serial PRIMARY KEY
);

CREATE TABLE matchTable (
	Name text,
	ID serial references playerInfo,
	winGame int,
	totalGame int
);