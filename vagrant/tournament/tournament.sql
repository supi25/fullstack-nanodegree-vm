-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


CREATE TABLE players (
 id serial PRIMARY KEY,
 name varchar(50) NOT NULL
);
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

CREATE VIEW player_details AS

SELECT p2.id AS id, p2.name AS name, win_counts.win_count AS wins, match_counts.match_count AS matches
FROM players AS p2
LEFT JOIN (
		SELECT p1.id AS p_id, count(m.id) AS win_count
		FROM players AS p1 LEFT JOIN matches AS m
		ON p1.id = m.player_id
		AND m.outcome = 'win'
		GROUP BY p1.id
	) AS win_counts
ON p2.id = win_counts.p_id
LEFT JOIN (
		SELECT p1.id AS p_id, count(m.id) AS match_count
		FROM players AS p1 LEFT JOIN matches AS m
		ON p1.id = m.player_id
		GROUP BY p1.id
	) AS match_counts
ON p2.id = match_counts.p_id;


-- SELECT EXISTS (
--                 SELECT 1
--                 FROM information_schema.tables
--                 WHERE table_name = 'player_details'
--             )


-- UPDATE players AS p2
-- SET wins = win_counts.win_count
-- FROM (
-- 		SELECT p1.id AS p_id, count(m.id) AS win_count
-- 		FROM players AS p1 JOIN matches AS m
-- 		ON p1.id = m.player_id
-- 		WHERE m.outcome = 'win'
-- 		GROUP BY p1.id
-- 	) AS win_counts
-- WHERE p2.id = win_counts.p_id;

-- UPDATE players AS p2
-- SET matches = match_counts.match_count
-- FROM (
-- 		SELECT p1.id AS p_id, count(m.id) AS match_count
-- 		FROM players AS p1 JOIN matches AS m
-- 		ON p1.id = m.player_id
-- 		GROUP BY p1.id
-- 	) AS match_counts
-- WHERE p2.id = match_counts.p_id