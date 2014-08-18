ABLESOCK v.00000000001

A ControlSurface python script to allow you to control
Ableton's transport and clip controls from any standard socket.

Examples would include an interactive art installation that fires
named clips in response to user input.

Features:
	Activate named clips and scenes via socket connection.
	It's very much a work in progress.

Notes: 
	Currently using port 6000. Alter in code as desired. Will
	automatically start playing the set when a connection
	is made. The current supported commands are:

	playclip <name>		: triggers the clip with name <name>
	stopclip <name>		: stops the clip with <name> from playing
	
	playscene <name>	: triggers the scene <name>

	stopall				: stops all clips from playing
	stop				: same as pressing stop on transport

