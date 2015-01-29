'''
Server code for the bat house at
Valencia State College, West Campus
Written by Toan Nguyen
1-22-15
toannguyen@knights.ucf.edu
'''

import multiprocessing
import time
import serialServer
import string
import batSend

def main():

	# sp object communicates data from the bathouse to the Pi
	# 
	taskQ = multiprocessing.Queue()
	resultQ = multiprocessing.Queue()
	sp = serialServer.SerialProcess(taskQ, resultQ)
	sp.daemon = True
	sp.start()

	# bs object communicates data from pi to GPRS
	batQ = multiprocessing.Queue()
	finishQ = multiprocessing.Queue()
	bs = batSend.SerialProcess(batQ, finishQ)
	bs.daemon = True
	bs.start()

	time.sleep(1)

	batInCount = 0
	batOutCount = 0
	batInTime = 0
	batInTime2 = 0
	batOutTime = 0
	batOutTime2 = 0
	incomingBat = 0
	outgoingBat = 0
	APIKEY = NULL


	while True:

		if not resultQ.empty():
			result = resultQ.get()
			print "Received data from bathouse: " + result


		##### Bat Counting System Logic #####
		# batInTime and batOutTime currently unused
		if result is "11" and incomingBat is 0 and outgoingBat is 0:
			incomingBat = 1
			batInTime = time.clock()
		else if result is "11" and incomingBat is 0 and outgoingBat is 1:
			outgoingBat = 0
			batOutCount++
			batOutTime2 = time.clock()
		else if result is "11" and incomingBat is 1 and outgoingBat is 1:
			outgoingBat = 0
			batOutCount++
			batOutTime2 = time.clock()
		else if result is "21" and incomingBat is 0 and outgoingBat is 0:
			outgoingBat = 1
			batOutTime = time.clock()
		else if result is "21" and incomingBat is 1 and outgoingBat is 0:
			incomingBat = 0
			batInCount++
			batInTime2 = time.clock()
		else if result is "21" and incomingBat is 1 and outgoingBat is 1:
			incomingBat = 0
			batInCount++
			batInTime2 = time.clock()

		# Every 30 minutes transmit data to Xively
		# data is wrapped in JSON
		if (int(time.strftime('%M', time.localtime()))%30) is 0:
			self.taskQ.put("temp")
			while not resultQ.empty():
				temp = resultQ.get()
				self.batQ.put("{\"method\": \"put\",\"resource\": \"/feeds/100441/\",\"params\"" +
					": {},\"headers\": {\"X-ApiKey\":\"" + APIKEY + "\"},\"body\": {\"version\": \"1.0.0\",\"datastreams\":")
				self.batQ.put("[{\"id\": \"01\",\"current_value\": \"" + batInCount + "\"},")
				self.batQ.put("[{\"id\": \"02\",\"current_value\": \"" + batOutCount + "\"},")
				self.batQ.put("[{\"id\": \"03\",\"current_value\": \"" + temp + "\"},")
				self.batQ.put("[{\"id\": \"04\",\"current_value\": \"" + "Ding!" + "\"}]},\"token\": \"token\"}")
				








		







			






if __name__ == '__main__':
	main()
