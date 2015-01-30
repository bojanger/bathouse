'''
Testing Python Script
to communicate with the GPRS shield through
command line
'''

import time
import multiprocessing
import serial


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
 				result = self.sp.readline().replace("\r\n", "")
 				print(result)



 		



if __name__ == '__main__':
	main()