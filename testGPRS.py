#!/usr/bin/python27

'''
Testing Python Script
to communicate with the GPRS shield through
command line
'''

import time
import multiprocessing
import serial

def main():
	taskQ = multiprocessing.Queue()
	resultQ = multiprocessing.Queue()
	sp = SerialProcess(taskQ, resultQ)
	sp.daemon = True
	sp.start()

	time.sleep(1)

	while True:

		if not resultQ.empty():
			while not resultQ.empty():
				result = resultQ.get()
				print "Received data from GPRS: " + result
				time.sleep(0.5)

		task = input("Enter command: ")
		if task is not '0':
			time.sleep(1)
		else:
			taskQ.put(task)

		time.sleep(1)




class SerialProcess(multiprocessing.Process):
 	
 	def __init__(self, taskQ, resultQ):
 		multiprocessing.Process.__init__(self)
 		self.taskQ = taskQ
 		self.resultQ = resultQ
 		self.usbPort = '/dev/tty.usbserial-A603QHNB'
 		self.sp = serial.Serial(self.usbPort, 192000, timeout=0)

 	def close(self):
 		self.sp.close()

 	def run(self):

 		self.sp.flushInput()

 		while True:

 			if not self.taskQ.empty():
 				task = self.taskQ.get()
 				self.sp.write(task + b'\r\n')

 			if self.sp.inWaiting() != 0:
 				result = self.sp.readline()
 				print(result)
 				self.resultQ.put(result)

main()