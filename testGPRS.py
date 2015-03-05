#!/usr/bin/python27

'''
Testing Python Script
to communicate with the GPRS shield through
command line
'''

import time
import multiprocessing
import serial
import serialServer

def main():
	taskQ = multiprocessing.Queue()
	resultQ = multiprocessing.Queue()
	sp = serialServer.SerialProcess(taskQ, resultQ)
	sp.daemon = True
	sp.start()

	time.sleep(1)

	input = raw_input
	task = input("Enter command: ")
	taskQ.put(task)

	while True:

		if resultQ.empty() is False:
			result = resultQ.get()
			print "Received data from GPRS: " + result
			task = input("Enter command: ")
			if task is None or task is '':
				time.sleep(1)
			else:
				taskQ.put(task)

class SerialProcess(multiprocessing.Process):
 	
 	def __init__(self, taskQ, resultQ):
 		multiprocessing.Process.__init__(self)
 		self.taskQ = taskQ
 		self.resultQ = resultQ
 		self.usbPort = '/dev/tty.usbserial-A603QHNB'
 		self.sp = serial.Serial(self.usbPort, 19200, timeout=0)

 	def close(self):
 		self.sp.close()

 	def run(self):

 		self.sp.flushInput()

 		while True:

 			if not self.taskQ.empty():
 				task = self.taskQ.get()
 				self.sp.write(task)

 			if self.sp.inWaiting() != 0:
 				result = self.sp.readline()
 				print(result)
 				self.resultQ.put(result)

main()