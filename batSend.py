#!/usr/bin/python27

import time
import multiprocessing
import serial

'''

def main():






if __name__ == "__main__":
	main()
'''
#Set constants

APN = "epc.tmobile.com"
HOSTSERVER = "api.xively.com"
HOSTPORT = 8081

class BatSend(multiprocessing.Process):

	def __init__(self, batQ, finishQ):
		multiprocessing.Process.__init__(self)
		self.batQ = batQ
		self.finishQ = finishQ
		self.usbPort = '/dev/ttyACM0'
		self.sp = serial.Serial(self.usbPort, 9600, timeout=1)

	def close(self):
		self.sp.close()

	def timedOut(self):
		timeOut = float(time.strftime("%s", time.localtime()))
		while self.sp.inWaiting() is not 1:
			if float(time.strftime("%s", time.localtime())) >= (timeOut + 30):
				print "tcpGSM timed out"
				return 0
		return 1

	# Method for getting an IP address and to initiate TCP communication
	def tcpGSM(self):
		self.sp.write(b'AT+CGATT?\r\n')
		if self.timedOut() is 0:
			return 0
		response = self.sp.readline()
		if response is "ERROR":
			return 0

		self.sp.write(b'AT+CSTT=\"" + APN + "\"\r\n')
		if self.timedOut() is 0:
			return 0
		response = self.sp.readline()
		if response is "ERROR":
			return 0

		self.sp.write(b'AT+CIICR\r\n')
		if self.timedOut is 0:
			return 0
		response = self.sp.readline()
		if response is "ERROR":
			return 0

		self.sp.write(b'AT+CIFSR\r\n')
		if self.timedOut is 0:
			return 0
		response = self.sp.readline()
		if response is "ERROR":
			return 0

		self.sp.write(b'AT+CIPSPRT=0\r\n')
		if self.timedOut is 0:
			return 0
		response = self.sp.readline()
		if response is "ERROR":
			return 0

		self.sp.write(b'AT+CIPSTART=\"tcp\",\"" + HOSTSERVER + "\",\"" + HOSTPORT + "\"\r\n')
		if self.timedOut is 0:
			return 0
		response = self.sp.readline()
		if response is "ERROR":
			return 0

		self.sp.write(b'AT+CIPSEND\r\n')
		if self.timedOut is 0:
			return 0
		response = self.sp.readline()
		if response is "ERROR":
			return 0

		print "Ready to send!"

		return 1



	def run(self):
		self.sp.flushInput()

		while True:

			if not self.batQ.empty():
				message = self.batQ.get()
				if self.tcpGSM() is 1:
					self.sp.write(message)
					while not self.batQ.empty():
						message = self.batQ.get()
						self.sp.write(message)
					self.sp.write((chr)26)
					if self.timedOut is 0:
						return
					response = self.sp.readline()
					if response is "ERROR":
						return
					self.sp.write(b'AT+CIPCLOSE\r\n')
					self.finishQ.put("Finished")




