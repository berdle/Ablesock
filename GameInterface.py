import Live

import time
import sys

sys.path.append("C:\\Python25\\lib")
import socket
import threading
import errno

from _Framework.ControlSurface import ControlSurface # Central base class for scripts based on the new Framework
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent # Base class for all classes encapsulating functions in Live

backref = None

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
inport = None
client = None
inport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
inport.bind(('127.0.0.1', 6000))
outport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class GameInterface(ControlSurface):
	__module__ = __name__
	__doc__ = "TCP Interface for ableton live"

	def __init__(self, c_instance):
		"""should set up the socket in here i guess?"""
		#self.log_message("Opening Socket")
		ControlSurface.__init__(self, c_instance)
		#self.set_suppress_rebuild_requests(True)
		global backref
		backref = self
		
		self.log_message("listening!")
		inport.listen(1)
		self.log_message("connection accepted sock open?")
		self.log_message("making new thread to listen")

		##self.log_message("trying method without thread: ")
		##self.run()

		myRun = Runner()
		t = threading.Thread(target = myRun.run)

		self.log_message("active threads = " + str(threading.activeCount()))
		self.log_message("starting new thread")
		t.start()
		self.log_message("active threads = " + str(threading.activeCount()))
		#self.log_message("waiting for join")
		#t.join()
		#self.log_message("passed join statement")
		#self.log_message("active threads = " + str(threading.activeCount()))
		
		


		#d = str(Live.Application.get_application().get_document().tracks)
		#l = str(Live.Song.__dict__)
		#self.log_message("List of attrs: \n " + d)
		#""" testing stuff """
		self.livedoc = Live.Application.get_application().get_document()

		self.log_message(str(dir(self.livedoc)))

		self.livedoc.add_current_song_time_listener(self.listen)


		#self.log_message("attrs for controlsurface = " + str(dir(self)))
		#for t in self.livedoc.tracks:
			#self.log_message("track details: " + str(dir(t)))
		#	for c in t.clip_slots:
				#self.log_message("clip details: " + str(dir(c.clip)))				
		#		if c.clip is not None:
		#			self.log_message("clip_name_is: " + c.clip.name)
		#			if c.clip.name == "shifted_arpeg":
		#				self.log_message("FIRING_CLIP")
		#				c.fire()

		#Live.Song.Song.start_playing(Live.Song.Song)
		#live_set.start_playing()

	def listen(self):
		#self.log_message("pop!")
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
					self.log_message(e)
			else:
				if len(data) > 0:
					self.log_message("got data: " + data)
					#tokenize and handle
					tok = data.split()
					if tok[0] == "playclip":
						for t in self.livedoc.tracks:
							for c in t.clip_slots:
								if c.clip is not None and c.clip.name == tok[1]:
									c.clip.fire()

						



	def run(self):
		"""wait on the socket?"""
		backref.log_message("in run")
		x = 0
		while x < 100:
			#backref.log_message("waiting for a connection")
			x = x + 1
			#(clientsocket, address) = inport.accept()

	#def update_display(self):
	#	self.log_message("update display was called!")


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
