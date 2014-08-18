Ablesock v0.1

A ControlSurface python script to allow you to control
Ableton's transport and clip controls from any standard socket.

Examples would include an interactive art installation that fires
named clips in response to user input.

Features:
	Activate named clips and scenes via socket connection.
	It's very much a work in progress.

Directions:<br> 
	Download the repository.<br> 
	Under the Ableton/Live n/Resources/Midi Remote Scripts/ folder<br>
	create a new folder with the name "Ablesock" (or whatever).<br>
	Place the *.py files into this folder. Start Ableton and from<br>
	the preferences->midi menu select thr name of your folder from<br>
	the control surfaces dropdown. It will initialise now.<br>
	<br>
	From your client application, open a socket to the host pc<br>
	(localhost or 127.0.0.1 if the same machine) using port 6000. <br>
	Ableton will begin playing when the connection is made. You will<br>
	now be able to send messages as plain text.<br>
	
Notes: 
	Currently using port 6000. Alter in code as desired. Will
	automatically start playing the set when a connection
	is made. The current supported commands are:

	playclip <name>		: triggers the clip with name <name>
	stopclip <name>		: stops the clip with <name> from playing
	
	playscene <name>	: triggers the scene <name>

	stopall				: stops all clips from playing
	stop				: same as pressing stop on transport

