from abc import ABC

import random  # for randint()


import trace_splitter.userDefinedMethods as userDefinedMethods 


class Request ( ABC ) :

    def __init__ ( self, timestamp, userID, size, details,reqType=None) :
        self.timestamp = timestamp
        self.userID = userID
        self.reqSize = size
        self.details = details
        self.reqType=reqType


    def getTimestamp ( self ) :
        return self.timestamp


    def getSize ( self ) :
        return self.reqSize


    def getRelativeSize ( self ) :
        return userDefinedMethods.sizeConversion ( self.reqSize, self.details [ 0 ] )


    def getUserID ( self ) :
        return self.userID


    def setTimestamp ( self, timestamp ) :
        self.timestamp = timestamp


    def setReqSize ( self, size ) :
        self.reqSize = size


    def setUserID ( self, userID ) :
        self.userID = userID


    def getSessionID ( self ) :
        return -1


    def getOutputString ( self ) :

        return_val=self.timestamp + ";;;" + str ( 0 ) + ";;;" + self.userID + ";;;" + str ( 0 ) + ";;;" + self.details [
            0 ] + ";" + self.details [ 1 ] + ";"
        return_val+=str(self.details[2])+";"+str(self.details[3])+";"+str(self.details[4])
        return return_val

class TraceReader ( ABC ) :

    def __init__ ( self, filename,reqType=None ) :
        self.filename = filename
        self.file = open ( self.filename, "r" )
        ''''TODO: open file'''
        self.i = 0
        print ( "OPEN R", filename )
        self.reqType=reqType
        return

    # for the structure arrival_time;;;start_time;;;user_id;;;end_time;;;request
    def readNextReq ( self,reqType=None ) :
        nextLine = self.file.readline ( )

        if nextLine == None :
            return nextLine
        line = str.split ( nextLine, ";;;" )
        if len ( line ) < 2 :
            return None
        
        startTime = line [ 0 ]
        user = line [ 2 ]
        subreq = str.split ( line [ 4 ], ";" )

        reqsize = len ( subreq [ 1 ] )
        details = [ subreq [ 0 ], subreq [ 1 ] ]
        subreq[-1]=subreq[-1].strip()
        details=[x for x in subreq]
        
        r = Request ( startTime, user, reqsize, details,reqType )
        return r


    def finish ( self ) :
        ''' flush and close file'''
        self.file.close ( )
        print ( "Close readers" )
        return

class TraceWriter ( ABC ) :

    def __init__ ( self, filename ) :
        self.filename = filename
        self.file = open ( self.filename, "w" )
        print ( "OPEN W", filename )
        return

    def writeNextReq ( self, req ) :
        self.file.write ( req.getOutputString ( ) + "\n" )
        return

    def finish ( self ) :
        self.file.close ( )
        print ( "Close writer" )
        return
