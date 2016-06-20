-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

\c tournament

CREATE TABLE players (
 id serial PRIMARY KEY,
 name varchar(50) NOT NULL
);

CREATE TABLE matches (
id serial PRIMARY KEY,
player_id integer references players(id),
opponent_id integer references players(id),
outcome varchar(25)
);

-- Return player id, number of wins
-- This is created as a separate view since it is used in multiple queries.
CREATE VIEW player_wins AS
SELECT p.id AS id, count(m.id) AS wins
FROM players AS p LEFT JOIN matches AS m
ON p.id = m.player_id
AND m.outcome = 'win'
GROUP BY p.id;

-- Return player id, player name, number of wins, number of matches, opponent match wins
-- This is created as a view instead of a table so that it will automatically update when
-- the list of players or matches is changed.
CREATE VIEW player_details AS
SELECT p.id AS id, p.name AS name, win_counts.wins AS wins, match_counts.match_count AS matches, player_omw.OMW AS OMW
FROM players AS p
LEFT JOIN player_wins AS win_counts
ON p.id = win_counts.id
LEFT JOIN (
		SELECT p.id AS p_id, count(m.id) AS match_count
		FROM players AS p LEFT JOIN matches AS m
		ON p.id = m.player_id
		GROUP BY p.id
	) AS match_counts
ON p.id = match_counts.p_id
LEFT JOIN (
	SELECT p.id AS p_id,
	CASE
		WHEN (sum(pw.wins) IS NULL) THEN
			0
		ELSE
			sum(pw.wins)
		END AS OMW
	FROM players AS p
	LEFT JOIN matches AS m
	ON m.player_id = p.id
	LEFT JOIN player_wins as pw
	ON pw.id = m.opponent_id
	GROUP BY p.id
) AS player_omw
ON p.id = player_omw.p_id;