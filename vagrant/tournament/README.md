#Tournament Results - Ryan Coughlan

Tournament Results is an API that provides functionality for tracking a Swiss Tournament

##Installation

Clone the GitHub repository or copy the contained files into a directory:

`$ git clone https://github.com/supi25/fullstack-nanodegree-vm`

####Files

- tournament.sql
- tournament.py
- tournament_test.py

##Usage

####Python Versions and Dependencies

Tournament Results supports python 2.7 and requires only the python 2.7 standard library.

####Provided Functions

- deleteMatches: Delete all tournament matches.
- deletePlayers: Delete all registered tournament players.
- countPlayers: Finds the number of player registered in the tournament.
- registerPlayer: Registers a player in the tournament.
- playerStandings: Ranks the players in the tournament.
- reportMatch: Records the outcome of a match.
- swissPairings: Generates the pairs of teams for the next round.

##Credit

This project is an extension of the material provided in Udacity's "Intro to Relational Databases" course, which includes the tournament.py file with function placeholders for most of the API functions, the tournament.sql file without any queries, and the tournament_test.py file. A small amount of content was added to tournament_test.py for this project, to account for changes in what the playerStandings function returns. This github repository was forked from udacity/fullstack-nanodegree-vm.

####Extended Functionality from Ryan Coughlan

- Definition of the tournament database, which includes definitions for:
	- players table
	- matches table
	- player_wins view
	- player_details view
- Definitions of the API functions in tournament.py
