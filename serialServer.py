# Python code to monitor data from bathouse and feed it to BatServer.py
# using multiprocessing.Queue()

import serial
import time
import multiprocessing

class SerialProcess(multiprocessing.Process):

	def __init__(self, taskQ, resultQ):
		multiprocessing.Process.__init__(self)
		self.taskQ = taskQ
		self.resultQ = resultQ
		self.usbPort = '/dev/ttyACM0' #Set usb port to bathouse
		self.sp = serial.Serial(self.usbPort, 9600, timeout=0)

	def close(self):
		self.sp.close()

	def run(self):

		self.sp.flushInput()

		while True:

			# Look for incoming requests from server thread using taskQ
			if not self.taskQ.empty():
				task = self.taskQ.get()
				self.sp.write(task + "\n")
			# Look for incoming requests from Arduino using resultQ
			if (self.sp.inWaiting() != 0):
				result = self.sp.readline().replace("\n","")
				self.resultQ.put(result)

				

