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
		self.usbPort = '/dev/tty.usbserial-A603QHNB' #Set usb port to bathouse
		self.sp = serial.Serial(self.usbPort, 19200, timeout=0)

	def close(self):
		self.sp.close()

	def run(self):

		self.sp.flushInput()

		while True:

			# Look for incoming requests from server thread using taskQ
			if not self.taskQ.empty():
				task = self.taskQ.get()
				self.sp.write(task)
			# Look for incoming requests from Arduino using resultQ
			result = self.sp.readline()
			if result is not None and result is not '':
				self.resultQ.put(result)

				

