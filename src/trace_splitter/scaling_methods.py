import math
import os
from math import *  # for ceil function
import numpy.random as np  # for random number generation np.random.rand(1)
import random  # for shuffling array random.shuffle()
from queue import PriorityQueue
from random import seed
from random import randint
# import trace_splitter.scaling as scaling
import scaling as scaling

'''TODO: server size difference'''
'''TODO: making # of jobs in servers equal by repeating/weight to balance'''


def timeSpanScaling ( inputFilename, factor ) :
	scale = 1 / factor  # if factor < 0  #TODO: for upscaling
	outputFilename = str.split ( inputFilename, "." ) [ 0 ] + "tspan.txt"

	reader = scaling.TraceReader ( inputFilename )
	writer = scaling.TraceWriter ( outputFilename )  # only one writer in random

	# for i in range(1, 10):
	nextReq = reader.readNextReq ( )
	while nextReq :
		# print("Next req read: ", nextReq.timestamp, nextReq.reqSize, nextReq.details)
		ts = int ( nextReq.timestamp )
		nextReq.timestamp = str ( int ( ts * scale ) )

		writer.writeNextReq ( nextReq )
		nextReq = reader.readNextReq ( )

	'''Close files'''
	reader.finish ( )
	writer.finish ( )

	return


def randomSampling ( inputFilename, factor, val ) :
	probability = factor  # if factor < 0  #TODO: for upscaling
	outputFilename = str.split ( inputFilename, "." ) [ 0 ] + "rand" + str ( val ) + ".txt"

	reader = scaling.TraceReader ( inputFilename )
	writer = scaling.TraceWriter ( outputFilename )  # only one writer in random

	# for i in range(1, 10):
	nextReq = reader.readNextReq ( )
	while nextReq :
		# print("Next req read: ", nextReq.timestamp, nextReq.reqSize, nextReq.details)
		if np.rand ( 1 ) <= probability :
			writer.writeNextReq ( nextReq )
		nextReq = reader.readNextReq ( )

	'''Close files'''
	reader.finish ( )
	writer.finish ( )

	return


def roundRobinSampling ( inputFilename, factor ) :
	numberOfServers = ceil ( 1 / factor )
	writer = [ 0 ] * numberOfServers
	currentServerIdx = 0

	reader = scaling.TraceReader ( inputFilename )
	for i in range ( 0, numberOfServers ) :  # range does [start, end)
		outputFilename = str.split ( inputFilename, "." ) [ 0 ] + str ( i + 1 ) + "rr.txt"
		writer [ i ] = scaling.TraceWriter ( outputFilename )

	nextReq = reader.readNextReq ( )
	while nextReq :
		# print(currentServerIdx, " Next req read: ", nextReq.timestamp, nextReq.reqSize, nextReq.details)
		writer [ currentServerIdx ].writeNextReq ( nextReq )
		currentServerIdx = (currentServerIdx + 1) % numberOfServers
		nextReq = reader.readNextReq ( )

	'''Close files'''
	reader.finish ( )
	for i in range ( 0, numberOfServers ) :  # range does [start, end)
		writer [ i ].finish ( )
	return


def roundRobinSamplingAll ( inputFilename, factor ) :
	numberOfnServers = int ( 1 // factor )
	numberOfxServers = 1
	if ceil ( 1 / factor ) == 1 // factor :
		print ( "Factor " + str ( ceil ( 1 / factor ) ) + " " + str ( 1 // factor ) )
		numberOfxServers = 0

	print ( "n servers = ", numberOfnServers, "numberOfxServers = ", numberOfxServers )

	serverWeight = [ 1 ] * numberOfnServers
	serverWeightX = 0
	p_x = 0
	p_resampling = 0
	p_n = 1

	if numberOfxServers == 1 :
		p_x = 1 - factor * numberOfnServers
		p_n = factor
		p_resampling = (p_n - p_x) / (1 - p_x)

	writer = [ 0 ] * numberOfnServers
	currentServerIdx = 0

	reader = scaling.TraceReader ( inputFilename )
	for i in range ( 0, numberOfnServers ) :  # range does [start, end)
		outputFilename = str.split ( inputFilename, "." ) [ 0 ] + str ( i + 1 ) + "rr.txt"
		writer [ i ] = scaling.TraceWriter ( outputFilename )
	if numberOfxServers == 1 :
		outputFilename = str.split ( inputFilename, "." ) [ 0 ] + "Xrr.txt"
		writerX = scaling.TraceWriter (
				outputFilename )  # fixme: do I need to initialize this beforehand? does it go out of scope?

	nextReq = reader.readNextReq ( )
	while nextReq :
		if random.random ( ) < p_x :
			writerX.writeNextReq ( nextReq )
		else :
			# print(currentServerIdx, " Next req read: ", nextReq.timestamp, nextReq.reqSize, nextReq.details)
			if random.random ( ) < p_resampling :
				writerX.writeNextReq ( nextReq )
			writer [ currentServerIdx ].writeNextReq ( nextReq )
			currentServerIdx = (currentServerIdx + 1) % numberOfnServers
		nextReq = reader.readNextReq ( )

	'''Close files'''
	reader.finish ( )
	for i in range ( 0, numberOfnServers ) :  # range does [start, end)
		writer [ i ].finish ( )
	if numberOfxServers == 1 :
		writerX.finish ( )
	return


def randomRoundRobinSampling ( inputFilename, factor ) :
	numberOfServers = ceil ( 1 / factor )
	writer = [ 0 ] * numberOfServers
	serverPriority = [ ]
	for i in range ( 0, numberOfServers ) :
		serverPriority.append ( i )
	random.shuffle ( serverPriority )
	currentServerIdx = 0

	reader = scaling.TraceReader ( inputFilename )
	for i in range ( 0, numberOfServers ) :  # range does [start, end)
		outputFilename = str.split ( inputFilename, "." ) [ 0 ] + str ( i + 1 ) + "randrr.txt"
		writer [ i ] = scaling.TraceWriter ( outputFilename )

	nextReq = reader.readNextReq ( )
	while nextReq :
		# print(serverPriority[currentServerIdx], " Next req read: ", nextReq.timestamp, nextReq.reqSize, nextReq.details)
		writer [ serverPriority [ currentServerIdx ] ].writeNextReq ( nextReq )
		currentServerIdx = (currentServerIdx + 1) % numberOfServers
		if currentServerIdx == 0 :
			random.shuffle ( serverPriority )
		nextReq = reader.readNextReq ( )

	'''Close files'''
	reader.finish ( )
	for i in range ( 0, numberOfServers ) :  # range does [start, end)
		writer [ i ].finish ( )

	return


def randomRoundRobinSamplingAll ( inputFilename, factor ) :
	numberOfnServers = int ( 1 // factor )
	numberOfxServers = 1
	if ceil ( 1 / factor ) == 1 // factor :
		print ( "Factor " + str ( ceil ( 1 / factor ) ) + " " + str ( 1 // factor ) )
		numberOfxServers = 0

	print ( "n servers = ", numberOfnServers, "numberOfxServers = ", numberOfxServers )

	serverWeight = [ 1 ] * numberOfnServers
	serverWeightX = 0
	p_x = 0
	p_resampling = 0
	p_n = 1
	if numberOfxServers == 1 :
		p_x = 1 - factor * numberOfnServers
		p_n = factor
		p_resampling = (p_n - p_x) / (1 - p_x)

	writer = [ 0 ] * numberOfnServers

	serverPriority = [ ]
	for i in range ( 0, numberOfnServers ) :
		serverPriority.append ( i )
	random.shuffle ( serverPriority )
	currentServerIdx = 0

	reader = scaling.TraceReader ( inputFilename )
	for i in range ( 0, numberOfnServers ) :  # range does [start, end)
		outputFilename = str.split ( inputFilename, "." ) [ 0 ] + str ( i + 1 ) + "randrr.txt"
		writer [ i ] = scaling.TraceWriter ( outputFilename )
	if numberOfxServers == 1 :
		outputFilename = str.split ( inputFilename, "." ) [ 0 ] + "Xrandrr.txt"
		writerX = scaling.TraceWriter (
				outputFilename )  # fixme: do I need to initialize this beforehand? does it go out of scope?

	nextReq = reader.readNextReq ( )
	while nextReq :
		if random.random ( ) < p_x :
			writerX.writeNextReq ( nextReq )
		else :
			# print(currentServerIdx, " Next req read: ", nextReq.timestamp, nextReq.reqSize, nextReq.details)
			if random.random ( ) < p_resampling :
				writerX.writeNextReq ( nextReq )
			writer [ serverPriority [ currentServerIdx ] ].writeNextReq ( nextReq )
			currentServerIdx = (currentServerIdx + 1) % numberOfnServers
			if currentServerIdx == 0 :
				random.shuffle ( serverPriority )
		# print(serverPriority)
		nextReq = reader.readNextReq ( )

	'''Close files'''
	reader.finish ( )
	for i in range ( 0, numberOfnServers ) :  # range does [start, end)
		writer [ i ].finish ( )
	if numberOfxServers == 1 :
		writerX.finish ( )

	return


'''Possible problem: Priority Queue has some blocking stuff. Should look into that'''


def leastWorkLeft ( inputFilename, factor ) :
	numberOfServers = ceil ( 1 / factor )

	writer = [ 0 ] * numberOfServers
	serverPriority = PriorityQueue ( )  # serverPriority queue has the tuple (totalReqSizeInThisQueue, queueIndex). It keeps track of amount of work in each queue and puts queue with least work left in the front
	for i in range ( 0, numberOfServers ) :
		serverPriority.put ( (0, i) )

	# currentServerIdx = 0

	reader = scaling.TraceReader ( inputFilename )
	for i in range ( 0, numberOfServers ) :  # range does [start, end)
		outputFilename = str.split ( inputFilename, "." ) [ 0 ] + str ( i + 1 ) + "lwl.txt"
		writer [ i ] = scaling.TraceWriter ( outputFilename )

	nextReq = reader.readNextReq ( )
	while nextReq :
		smallestq = serverPriority.get ( )
		if smallestq is None :
			print ( "Queue empty" )
		# print(" Next req read: ", nextReq.timestamp, nextReq.reqSize, "in queue ", smallestq[1], "of size ", smallestq[0])

		writer [ smallestq [ 1 ] ].writeNextReq ( nextReq )
		newSize = smallestq [ 0 ] + nextReq.getRelativeSize ( )
		# print("$$$$$$$$" , newSize, smallestq[1])
		serverPriority.put ( (newSize, smallestq [ 1 ]) )
		nextReq = reader.readNextReq ( )

	'''Close files'''
	reader.finish ( )
	for i in range ( 0, numberOfServers ) :  # range does [start, end)
		writer [ i ].finish ( )

	return


'''Possible problem: Priority Queue has some blocking stuff. Should look into that'''


def leastWorkLeftAll ( inputFilename, factor,reqType ) :
	# numberOfServers = ceil(1/factor)
	print("factor: ",factor," floor: ",floor(1 / factor))
	numberOfnServers = int (floor(( 1 / factor )))
	numberOfxServers = 1
	# print ( "Factor " + str ( ceil ( 1 / factor ) ) + " " + str ( floor(1 / factor) ) )
	if ceil ( 1 / factor ) == int(floor(1 / factor)) :
		print ( "Factor " + str ( ceil ( 1 / factor ) ) + " " + str (floor( 1 / factor ) ))
		numberOfxServers = 0

	print ( "n servers = ", numberOfnServers, "numberOfxServers = ", numberOfxServers )

	serverWeight = [ 1 ] * numberOfnServers
	serverWeightX = 0
	p_x = 0
	p_resampling = 0
	p_n = 1
	if numberOfxServers == 1 :
		p_x = 1 - factor * numberOfnServers
		p_n = factor
		p_resampling = (p_n - p_x) / (1 - p_x)

	writer = [ 0 ] * numberOfnServers

	serverPriority = PriorityQueue ( )  # serverPriority queue has the tuple (totalReqSizeInThisQueue, queueIndex). It keeps track of amount of work in each queue and puts queue with least work left in the front
	for i in range ( 0, (numberOfnServers + numberOfxServers) ) :
		serverPriority.put ( (0, i) )

	reader = scaling.TraceReader ( inputFilename,reqType = reqType )
	traceFileNames = [ ]
	for i in range ( 0, numberOfnServers ) :  # range does [start, end)
		outputFilename = str.split ( inputFilename, "." ) [ 0 ] + str ( i + 1 ) + "lwl.txt"
		traceFileNames.extend ( [ outputFilename ] )
		writer [ i ] = scaling.TraceWriter ( outputFilename )
	if numberOfxServers == 1 :
		outputFilename = str.split ( inputFilename, "." ) [ 0 ] + "Xlwl.txt"
		traceFileNames.extend ( [ outputFilename ] )
		writerX = scaling.TraceWriter (
				outputFilename )  # fixme: do I need to initialize this beforehand? does it go out of scope?
	# ,
	nextReq = reader.readNextReq ( reqType = reqType )
	while nextReq :
		smallestq = serverPriority.get ( )
		if smallestq is None :
			print ( "Queue empty" )
		# print(" Next req read: ", nextReq.timestamp, nextReq.reqSize, "in queue ", smallestq[1], "of size ", smallestq[0])

		if smallestq [ 1 ] == numberOfnServers :
			writerX.writeNextReq ( nextReq )
			newSize = smallestq [ 0 ] + (1 / p_x * nextReq.getRelativeSize ( ))
		else :
			writer [ smallestq [ 1 ] ].writeNextReq ( nextReq)
			newSize = smallestq [ 0 ] + (1 / p_n * nextReq.getRelativeSize ( ))
			if random.random ( ) < p_resampling :
				writerX.writeNextReq ( nextReq )
		# print("$$$$$$$$" , newSize, smallestq[1])
		serverPriority.put ( (newSize, smallestq [ 1 ]) )
		nextReq = reader.readNextReq (reqType = reqType )

	'''Close files'''
	reader.finish ( )
	for i in range ( 0, numberOfnServers ) :  # range does [start, end)
		writer [ i ].finish ( )
	if numberOfxServers == 1 :
		writerX.finish ( )

	return traceFileNames


'''Possible problem: Priority Queue has some blocking stuff. Should look into that'''


def joinShortestQ ( inputFilename, factor ) :
	numberOfServers = ceil ( 1 / factor )
	writer = [ 0 ] * numberOfServers
	serverPriority = PriorityQueue ( )  # serverPriority queue has the tuple (totalNumberOfRequestInThisQueue, queueIndex). It keeps track of amount of work in each queue and puts queue with least work left in the front
	for i in range ( 0, numberOfServers ) :
		serverPriority.put ( (0, i) )

	# currentServerIdx = 0

	reader = scaling.TraceReader ( inputFilename )
	for i in range ( 0, numberOfServers ) :  # range does [start, end)
		outputFilename = str.split ( inputFilename, "." ) [ 0 ] + str ( i + 1 ) + "jsq.txt"
		writer [ i ] = scaling.TraceWriter ( outputFilename )

	nextReq = reader.readNextReq ( )
	while nextReq :
		smallestq = serverPriority.get ( )
		if smallestq is None :
			print ( "Queue empty" )
		# print(" Next req read: ", nextReq.timestamp, nextReq.reqSize, nextReq.details, "in queue ", smallestq[1], "of size ", smallestq[0])

		writer [ smallestq [ 1 ] ].writeNextReq ( nextReq )
		newCount = smallestq [ 0 ] + 1
		# print("$$$$$$$$" , newCount, smallestq[1])
		serverPriority.put ( (newCount, smallestq [ 1 ]) )
		nextReq = reader.readNextReq ( )

	'''Close files'''
	reader.finish ( )
	for i in range ( 0, numberOfServers ) :  # range does [start, end)
		writer [ i ].finish ( )

	return


'''First check if session is in play. If yes, add to that server. Else, add to shortest Q '''


def joinShortestQSticky ( inputFilename, factor ) :
	numberOfServers = ceil ( 1 / factor )
	writer = [ 0 ] * numberOfServers
	serverPriority = { }
	# serverSessions = [set()] * numberOfServers
	serverSessions = [ ]
	for i in range ( 0, numberOfServers ) :
		serverPriority [ i ] = 0
		serverSessions.append ( set ( ) )

	print ( "server sessions", serverSessions )

	reader = scaling.TraceReader ( inputFilename )
	for i in range ( 0, numberOfServers ) :  # range does [start, end)
		outputFilename = str.split ( inputFilename, "." ) [ 0 ] + str ( i + 1 ) + "jsqs.txt"
		writer [ i ] = scaling.TraceWriter ( outputFilename )

	nextReq = reader.readNextReq ( )
	while nextReq :
		session = nextReq.getSessionID ( )
		print ( "\nRequest ", nextReq.timestamp, nextReq.reqSize, "Session", session )

		nextServer = -1
		if session != -1 :
			for i in range ( 0, len ( serverSessions ) ) :
				if session in serverSessions [ i ] :
					nextServer = i
					break

		if nextServer == -1 :
			# did not find session in server. Server based on JSQ
			nextServer = min ( serverPriority, key = serverPriority.get )

		print ( "Next req read: ", nextReq.timestamp, nextReq.reqSize, nextReq.getSessionID ( ), nextReq.details,
				"in queue ", nextServer )

		writer [ nextServer ].writeNextReq ( nextReq )
		newCount = serverPriority [ nextServer ] + 1
		serverPriority [ nextServer ] = newCount

		if session != -1 :
			serverSessions [ nextServer ].add ( session )

		nextReq = reader.readNextReq ( )

	'''Close files'''
	reader.finish ( )
	for i in range ( 0, numberOfServers ) :  # range does [start, end)
		writer [ i ].finish ( )

	return


'''First check if session is in play. If yes, add to that server. Else, add to shortest Q '''


def leastWorkLeftSticky ( inputFilename, factor ) :
	numberOfServers = ceil ( 1 / factor )
	writer = [ 0 ] * numberOfServers
	serverPriority = { }
	# serverSessions = [set()] * numberOfServers
	serverSessions = [ ]
	for i in range ( 0, numberOfServers ) :
		serverPriority [ i ] = 0
		serverSessions.append ( set ( ) )

	print ( "server sessions", serverSessions )

	reader = scaling.TraceReader ( inputFilename )
	for i in range ( 0, numberOfServers ) :  # range does [start, end)
		outputFilename = str.split ( inputFilename, "." ) [ 0 ] + str ( i + 1 ) + "lwls.txt"
		writer [ i ] = scaling.TraceWriter ( outputFilename )

	nextReq = reader.readNextReq ( )
	while nextReq :
		session = nextReq.getSessionID ( )
		print ( "\nRequest ", nextReq.timestamp, nextReq.reqSize, "Session", session )

		nextServer = -1
		if session != -1 :
			for i in range ( 0, len ( serverSessions ) ) :
				if session in serverSessions [ i ] :
					nextServer = i
					break

		if nextServer == -1 :
			# did not find session in server. Server based on JSQ
			nextServer = min ( serverPriority, key = serverPriority.get )

		print ( "Next req read: ", nextReq.timestamp, nextReq.reqSize, nextReq.getSessionID ( ), nextReq.details,
				"in queue ", nextServer )

		writer [ nextServer ].writeNextReq ( nextReq )
		newSize = serverPriority [ nextServer ] + nextReq.getRelativeSize ( )
		serverPriority [ nextServer ] = newSize

		if session != -1 :
			serverSessions [ nextServer ].add ( session )

		nextReq = reader.readNextReq ( )

	'''Close files'''
	reader.finish ( )
	for i in range ( 0, numberOfServers ) :  # range does [start, end)
		writer [ i ].finish ( )

	return


def testing ( inputFilename, factor ) :
	numberOfnServers = int ( 1 // factor )
	numberOfxServers = 1
	if ceil ( 1 / factor ) == 1 // factor :
		print ( "Factor " + str ( ceil ( 1 / factor ) ) + " " + str ( 1 // factor ) )
		numberOfxServers = 0

	print ( "n servers = ", numberOfnServers, "numberOfxServers = ", numberOfxServers )

	serverWeight = [ 0 ] * numberOfnServers
	serverWeightX = 0

	p_x = 1 - factor * numberOfnServers
	p_n = factor
	w_n = p_x / p_n

	for i in range ( 0, numberOfnServers ) :
		serverWeight [ i ] = w_n
	if numberOfxServers == 1 :
		serverWeightX = 1

	print ( "Weights= ", serverWeight, " and extra server ", serverWeightX, p_x, w_n )

	return


def modelBasedSimple ( inputFilename, factor ) :
	bucketSize = 20 * 1000000000  # in nanoseconds, same unit as timestamp in file

	scale = 1 / factor  # if factor < 0  #TODO: for upscaling
	outputFilename = str.split ( inputFilename, "." ) [ 0 ] + "modelSimple.txt"

	reader = scaling.TraceReader ( inputFilename )
	writer = scaling.TraceWriter ( outputFilename )  # only one writer in model Based

	nextReq = reader.readNextReq ( )

	'''Update timestamp and bucket initially'''
	timeStamp1 = float ( nextReq.timestamp )
	timeStamp2 = timeStamp1 + bucketSize
	# print("Bucket of ", timeStamp1, timeStamp2)

	while nextReq :
		requestList = [ ]
		while nextReq :
			requestList.append ( nextReq )
			nextReq = reader.readNextReq ( )
			if nextReq is None :
				break
			# print("Next req read: ", nextReq.timestamp, nextReq.reqSize, nextReq.getSessionID())
			if float ( nextReq.timestamp ) > timeStamp2 :
				break

		numberOfNewReq = round ( len ( requestList ) * factor )
		# print("Generate Timestamps for ", numberOfNewReq, " requests")
		timestamps = [ ]
		seed ( 1 )
		for i in range ( 0, numberOfNewReq ) :
			timestamps.append ( randint ( timeStamp1, timeStamp2 ) )
		timestamps = sorted ( timestamps )
		# print("Generated Timestamps ", timestamps)

		seed ( 1 )
		for i in range ( 0, numberOfNewReq ) :
			randReqIdx = randint ( 0, len ( requestList ) - 1 )
			# print("Rnad in range 0, ", len(requestList)-1, randReqIdx)
			newReq = requestList [ randReqIdx ]
			newReq.setTimestamp ( str ( timestamps [ i ] ) )
			# print("New req written: ", newReq.timestamp, newReq.reqSize, newReq.getSessionID())
			writer.writeNextReq ( newReq )

		'''Update timestamp and bucket'''
		timeStamp1 = timeStamp2
		timeStamp2 = timeStamp1 + bucketSize
	# print("Bucket of ", timeStamp1, timeStamp2)

	'''Close files'''
	reader.finish ( )
	writer.finish ( )

	return


def moveDownscaledTracesToCorrectFolders ( traceFilePaths ) :
	print('\n'.join(traceFilePaths))
	# cmd=["mkdir","-p",directoryPath]
	filePathSplits=traceFilePaths[0].split("/")[:-1]
	rootPath="/".join(filePathSplits)+"/downscaledTraces"
	for x in traceFilePaths:
		traceName=x.split("/")[-1].split(".")[0]

		dirName=rootPath+"/"+traceName+"/base/input"
		# dirName = '"' + dirName + '"'
		cmd='mkdir -p "'+dirName+'"'
		print("cmd 1:",cmd)
		os.system(cmd)

		# x2='"'+x+'"'
		cmd='mv "'+x+'" "'+dirName+'/'+traceName+'.txt"'
		os.system(cmd)
		print ( "cmd 2:", cmd )
		print(traceName)

		dirName2 = rootPath + "/" + traceName + "/base/output"
		dirName2='"'+dirName2+'"'
		cmd = "mkdir -p " + dirName2
		print ( "cmd 3:", cmd )
		os.system ( cmd )


		dirName2 = rootPath + "/" + traceName + "/base/periodTraces"
		dirName2 = '"' + dirName2 + '"'
		cmd = "mkdir -p " + dirName2
		print ( "cmd 4:", cmd )
		os.system ( cmd )
	# print("/".join(filePathSplits))

	return


def downscaleTrace ( traceFilePath, downscalingFactor, downscalingMethod,reqType=None ) :
	if downscalingMethod == "lwl" :
		traceFilePaths = leastWorkLeftAll ( inputFilename = traceFilePath, factor = downscalingFactor,reqType = reqType )
		# moveDownscaledTracesToCorrectFolders(traceFilePaths)

	else :
		print ( "invalid downscaling method selection" )
	return


def main ( ) :
	print ( "Main" )
	# inputFile = "/Users/sxs2561/Documents/dummy_trial_code/python/trace/upscaleTest1/output/trace.txt"
	inputFile="/Users/sxs2561/Documents/Research/trace_scaler/TraceScaler/src/files/source_trace.txt"
	# inputFile = "/Users/rxh655/OneDrive - The Pennsylvania State University/Research/TraceScaler/trace_files/random/v2/trace1_rate100.txt"
	# roundRobinSamplingAll(inputFile, .5)
	# scalingFactor = 0.75
	#
	# modelBasedSimple(inputFile, scalingFactor)
	# timeSpanScaling(inputFile, scalingFactor)
	# randomSampling(inputFile, scalingFactor)
	# randomRoundRobinSamplingAll(inputFile, scalingFactor)
	# roundRobinSamplingAll(inputFile, scalingFactor)
	# leastWorkLeftAll(inputFile, scalingFactor)

	# modelBasedSimple(inputFile, .5)
	# timeSpanScaling(inputFile, .5)
	# randomSampling(inputFile, .5, "6")
	# randomRoundRobinSampling(inputFile, .5)
	# roundRobinSampling(inputFile, .5)
	# leastWorkLeft(inputFile, .5)
	# leastWorkLeftAll ( inputFile, .5 )
	downscaleTrace(inputFile,0.25,"lwl")


# for i in range(7, 11):
#     randomSampling(inputFile, .5, i)
#
# return


if __name__ == "__main__" :
	main ( )
