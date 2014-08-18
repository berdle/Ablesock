ABLESOCK v.00000000001

A ControlSurface python script to allow you to control
Ableton's transport and clip controls from any standard socket.

Examples would include an interactive art installation that fires
named clips in response to user input.

Features:
	Activate named clips via socket connection.
	Nothing much else! It's very much a work in progress
	and today is day 1.

Notes: 
	Currently using port 6000. Alter in code as desired. Will
	automatically start playing the set when a connection
	is made. The current single supported command is 

	playclip <name>		: triggers the clip with name <name>

