-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


-- CREATE TABLE players (
--  id serial PRIMARY KEY,
--  name varchar(50) NOT NULL,
--  wins integer,
--  matches integer,
--  best_opponent_wins integer
-- );
-- CREATE TABLE matches (
-- id serial PRIMARY KEY,
-- player_id integer references players(id),
-- opponent_id integer references players(id),
-- outcome varchar(25)
-- );

-- INSERT INTO players (name, wins, matches, best_opponent_wins) VALUES ('dave', 0, 0, 0);
SELECT count(id) FROM players;