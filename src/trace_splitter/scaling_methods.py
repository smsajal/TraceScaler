import math
import os
from math import *  # for ceil function
import numpy.random as np  # for random number generation np.random.rand(1)
import random  # for shuffling array random.shuffle()
from queue import PriorityQueue
from random import seed
from random import randint

import trace_splitter.scaling as scaling



def timeSpanScaling ( inputFilename, factor ) :
	scale = 1 / factor 
	outputFilename = str.split ( inputFilename, "." ) [ 0 ] + "tspan.txt"

	reader = scaling.TraceReader ( inputFilename )
	
	
	writer = scaling.TraceWriter ( outputFilename )  # only one writer in random

	
	nextReq = reader.readNextReq ( )
	while nextReq :
		
		ts = int ( nextReq.timestamp )
		nextReq.timestamp = str ( int ( ts * scale ) )

		writer.writeNextReq ( nextReq )
		nextReq = reader.readNextReq ( )

	'''Close files'''
	reader.finish ( )
	writer.finish ( )

	print(f"==============\noutput file path: {outputFilename}\n")

	return


def randomSampling ( inputFilename, factor, val='' ) :
	probability = factor  # if factor < 0  #TODO: for upscaling
	outputFilename = str.split ( inputFilename, "." ) [ 0 ] + "rand" + str ( val ) + ".txt"

	reader = scaling.TraceReader ( inputFilename )
	writer = scaling.TraceWriter ( outputFilename )  

	
	nextReq = reader.readNextReq ( )
	while nextReq :
		
		if np.rand ( 1 ) <= probability :
			writer.writeNextReq ( nextReq )
		nextReq = reader.readNextReq ( )

	'''Close files'''
	reader.finish ( )
	writer.finish ( )
	print(f"==============\noutput file path: {outputFilename}\n")
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
	outputFilenames=[]
	for i in range ( 0, numberOfnServers ) :  # range does [start, end)
		outputFilename = str.split ( inputFilename, "." ) [ 0 ] + str ( i + 1 ) + "rr.txt"
		outputFilenames.append(outputFilename)
		writer [ i ] = scaling.TraceWriter ( outputFilename )
	if numberOfxServers == 1 :
		outputFilename = str.split ( inputFilename, "." ) [ 0 ] + "Xrr.txt"
		outputFilenames.append(outputFilename)
		writerX = scaling.TraceWriter (
				outputFilename ) 

	nextReq = reader.readNextReq ( )
	while nextReq :
		if random.random ( ) < p_x :
			writerX.writeNextReq ( nextReq )
		else :
			
			if random.random ( ) < p_resampling :
				writerX.writeNextReq ( nextReq )
			writer [ currentServerIdx ].writeNextReq ( nextReq )
			currentServerIdx = (currentServerIdx + 1) % numberOfnServers
		nextReq = reader.readNextReq ( )

	'''Close files'''
	reader.finish ( )
	for i in range ( 0, numberOfnServers ) :  
		writer [ i ].finish ( )
	if numberOfxServers == 1 :
		writerX.finish ( )
	print(f"==============\noutput file path: \n{chr(10).join(outputFilenames)}\n")
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

	outputFilenames=[]
	reader = scaling.TraceReader ( inputFilename )
	for i in range ( 0, numberOfnServers ) : 
		outputFilename = str.split ( inputFilename, "." ) [ 0 ] + str ( i + 1 ) + "randrr.txt"
		outputFilenames.append(outputFilename)
		writer [ i ] = scaling.TraceWriter ( outputFilename )
	if numberOfxServers == 1 :
		outputFilename = str.split ( inputFilename, "." ) [ 0 ] + "Xrandrr.txt"
		outputFilenames.append(outputFilename)
		writerX = scaling.TraceWriter (
				outputFilename )  

	nextReq = reader.readNextReq ( )
	while nextReq :
		if random.random ( ) < p_x :
			writerX.writeNextReq ( nextReq )
		else :
			
			if random.random ( ) < p_resampling :
				writerX.writeNextReq ( nextReq )
			writer [ serverPriority [ currentServerIdx ] ].writeNextReq ( nextReq )
			currentServerIdx = (currentServerIdx + 1) % numberOfnServers
			if currentServerIdx == 0 :
				random.shuffle ( serverPriority )
		
		nextReq = reader.readNextReq ( )

	'''Close files'''
	reader.finish ( )
	for i in range ( 0, numberOfnServers ) :  # range does [start, end)
		writer [ i ].finish ( )
	if numberOfxServers == 1 :
		writerX.finish ( )
	print(f"==============\noutput file path: \n{chr(10).join(outputFilenames)}\n")
	return




def leastWorkLeftAll ( inputFilename, factor ) :
	
	print("factor: ",factor," floor: ",floor(1 / factor))
	numberOfnServers = int (floor(( 1 / factor )))
	numberOfxServers = 1
	
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

	reader = scaling.TraceReader ( inputFilename )
	
	traceFileNames = [ ]
	for i in range ( 0, numberOfnServers ) :  
		outputFilename = str.split ( inputFilename, "." ) [ 0 ] + str ( i + 1 ) + "lwl.txt"
		traceFileNames.extend ( [ outputFilename ] )
		writer [ i ] = scaling.TraceWriter ( outputFilename )
	if numberOfxServers == 1 :
		outputFilename = str.split ( inputFilename, "." ) [ 0 ] + "Xlwl.txt"
		traceFileNames.extend ( [ outputFilename ] )
		writerX = scaling.TraceWriter (
				outputFilename ) 
	# ,
	nextReq = reader.readNextReq (  )
	while nextReq :
		smallestq = serverPriority.get ( )
		if smallestq is None :
			print ( "Queue empty" )
		

		if smallestq [ 1 ] == numberOfnServers :
			writerX.writeNextReq ( nextReq )
			newSize = smallestq [ 0 ] + (1 / p_x * nextReq.getRelativeSize ( ))
		else :
			writer [ smallestq [ 1 ] ].writeNextReq ( nextReq)
			newSize = smallestq [ 0 ] + (1 / p_n * nextReq.getRelativeSize ( ))
			if random.random ( ) < p_resampling :
				writerX.writeNextReq ( nextReq )
		
		serverPriority.put ( (newSize, smallestq [ 1 ]) )
		nextReq = reader.readNextReq ( )

	'''Close files'''
	reader.finish ( )
	for i in range ( 0, numberOfnServers ) :  
		writer [ i ].finish ( )
	if numberOfxServers == 1 :
		writerX.finish ( )
	print(f"==============\noutput file path: \n{chr(10).join(traceFileNames)}\n")
	
	return




def avgRateScaling ( inputFilename, factor,bucketSize ) :
	bucketSize = 20 * 1000000000  # in nanoseconds, same unit as timestamp in file

	scale = 1 / factor  # if factor < 0  #TODO: for upscaling
	outputFilename = str.split ( inputFilename, "." ) [ 0 ] + "modelSimple.txt"

	reader = scaling.TraceReader ( inputFilename )
	writer = scaling.TraceWriter ( outputFilename )  # only one writer in model Based

	nextReq = reader.readNextReq ( )

	'''Update timestamp and bucket initially'''
	timeStamp1 = float ( nextReq.timestamp )
	timeStamp2 = timeStamp1 + bucketSize
	

	while nextReq :
		requestList = [ ]
		while nextReq :
			requestList.append ( nextReq )
			nextReq = reader.readNextReq ( )
			if nextReq is None :
				break
			
			if float ( nextReq.timestamp ) > timeStamp2 :
				break

		numberOfNewReq = round ( len ( requestList ) * factor )
		
		timestamps = [ ]
		seed ( 1 )
		for i in range ( 0, numberOfNewReq ) :
			timestamps.append ( randint ( timeStamp1, timeStamp2 ) )
		timestamps = sorted ( timestamps )
		

		seed ( 1 )
		for i in range ( 0, numberOfNewReq ) :
			randReqIdx = randint ( 0, len ( requestList ) - 1 )
			newReq = requestList [ randReqIdx ]
			newReq.setTimestamp ( str ( timestamps [ i ] ) )
			writer.writeNextReq ( newReq )

		'''Update timestamp and bucket'''
		timeStamp1 = timeStamp2
		timeStamp2 = timeStamp1 + bucketSize
	

	'''Close files'''
	reader.finish ( )
	writer.finish ( )
	print(f"==============\noutput file path: \n{outputFilename}\n")
	return
