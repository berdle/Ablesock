import Live

import time
import sys

# alter this to point to your python libs. using 2.5.1 as is version supported by Ableton Live 8
sys.path.append("C:\\Python25\\lib")
import socket
import threading
import errno

from _Framework.ControlSurface import ControlSurface # Central base class for scripts based on the new Framework
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent # Base class for all classes encapsulating functions in Live

backref = None
inport = None
client = None

TCP_IP = '127.0.0.1'
TCP_PORT = 6000
BUFFER_SIZE = 1024

# todo - move these !
inport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
inport.bind((TCP_IP, TCP_PORT))
outport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

""" Main class - contains song_timer_listener that drives the socket reading """
class GameInterface(ControlSurface):
	__module__ = __name__
	__doc__ = "TCP Interface for ableton live"

	def __init__(self, c_instance):
		ControlSurface.__init__(self, c_instance)
		#self.set_suppress_rebuild_requests(True) --causes errors?
		global backref
		backref = self
		
		self.log_message("listening!")
		self.log_message("CONTROL_SURFACE_DETAILS")
		self.log_message(str(dir(ControlSurface)))
		inport.listen(1)
		myRun = Runner()
		t = threading.Thread(target = myRun.run)
		self.log_message("starting accept thread")
		t.start()
		self.livedoc = Live.Application.get_application().get_document()
		self.log_message(str(dir(self.livedoc)))
		self.livedoc.add_current_song_time_listener(self.listen)


	def listen(self):
		global client
		if client is not None:
			try:
				data = client.recv(BUFFER_SIZE)
			except socket.error, e:
				err = e.args[0]
				if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
					# ignore
					data = None
				else:
					self.log_message("*** EXCEPTION ***")
					self.log_message(str(e))
			else:
				if len(data) > 0:
					self.log_message("got data: " + data)
					# todo: refactor this out 
					tok = data.split()
					if tok[0] == "playclip":
						slot = self.findclip(tok[1])
						if slot is not None:
							slot.fire()
					
					elif tok[0] == "stopclip":
						slot = self.findclip(tok[1])
						if slot is not None:
							slot.stop()
					
					elif tok[0] == "stopall":
						self.livedoc.stop_all_clips()
					
					elif tok[0] == "stop":
						self.livedoc.stop_playing()
					
					elif tok[0] == "playscene":    #todo: playscene <index> or playscene <name>
						scene = self.findscene(tok[1])
						if scene is not None:
							scene.fire()

					#elif tok[0] == "cc":

					#elif tok[0] == "tempo":
					#	tempo = int(tok[1])
					#	if tempo is not None:
					#		self.livedoc.tempo(tempo)



	""" Finds the named clip and returns a reference to the containing slot """
	def findclip(self, name):
		for t in self.livedoc.tracks:
			for c in t.clip_slots:
				if c.clip is not None and c.clip.name == name:
					return c
		return None

	""" finds the named scene and returns its object """
	def findscene(self, name):
		for s in self.livedoc.scenes:
			if s is not None and s.name == name:
				return s
		return None

""" this accepts incoming connections """
class Runner():
	def run(self):
		global inport		
		global client
		(clientsocket, address) = inport.accept()
		clientsocket.setblocking(0)
		client = clientsocket
		Live.Application.get_application().get_document().start_playing()
		
		#myHandler = Handler()		
		#cthread = threading.Thread(target = myHandler.run)
		#cthread.start()
		
		#for t in self.livedoc.tracks:
		#	for c in t.clip_slots:
		#		if c.clip.name == "shifted_arpeg":
		#			c.clip.fire()
		#
		
""" possibly deprecated as the update frequency is ~100ms vs. ~60ms for the current_song_time listener """
""" may still require to handle start messages when the song is not playing """
class Handler():
	def run(self):
		global client
		livedoc = Live.Application.get_application().get_document()
		
		#if client is not None:
		#	livedoc.start_playing()
		
		while 1:
			input = client.recv(BUFFER_SIZE)
			## need tokenizing? prob a fully easy split function
			tokens = input.split()
			##livedoc.start_playing()
			
			#client.send(tokens[0] + "\n")

			if tokens[0][0] == "p":
				livedoc.start_playing()

			if tokens[0] == "s":
				livedoc.stop_playing()
