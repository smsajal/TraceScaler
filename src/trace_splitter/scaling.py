from abc import ABC, abstractmethod

import random  # for randint()

# import trace_splitter.userDefinedMethods as userDefinedMethods 
import userDefinedMethods as userDefinedMethods 


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
        # return self.timestamp + ";;;" + self.userID + ";;;" + str(0) + ";;;" + self.details[0] + ";" + self.details[1] + ";" + str(0)

        # print(" ---- details: ",self.details)
        return_val=self.timestamp + ";;;" + str ( 0 ) + ";;;" + self.userID + ";;;" + str ( 0 ) + ";;;" + self.details [
            0 ] + ";" + self.details [ 1 ] + ";"
        if self.reqType=="BlockDevice":
            return_val+=str(self.details[2])
        elif self.details[0] in ["HOME_TIMELINE","USER_TIMELINE"]: #this is default for tracescaler
            return_val+=str(self.details[2])+";"+str(self.details[3])+";"+str(self.details[4])
        else:
            return_val+=str(0)
        return return_val


class SessionReq ( Request ) :

    def __init__ ( self, timestamp, size, sessionID, details ) :
        super ( SessionReq, self ).__init__ ( timestamp, size, details )
        self.sessionID = sessionID


    def getSessionID ( self ) :
        return self.sessionID


class TraceReader ( ABC ) :

    def __init__ ( self, filename,reqType=None ) :
        self.filename = filename
        self.file = open ( self.filename, "r" )
        ''''TODO: open file'''
        self.i = 0
        print ( "OPEN R", filename )
        self.reqType=reqType
        return


    '''TODO: Handle subrequest'''
    ## for the structure arrival_time;;;user_id;;;end_time;;;request
    # def readNextReq(self):
    #     nextLine = self.file.readline()
    #     if nextLine == None:
    #         return nextLine
    #     line = str.split(nextLine, ";;;")
    #     if len(line) < 2:
    #         return None
    #     startTime = line[0]
    #     user = line[1]
    #     subreq = str.split(line[3], ";")
    #     reqsize = len(subreq[1])
    #     details = [subreq[0], subreq[1]]
    #     r = Request(startTime, user, reqsize, details)
    #     return r
    #     #self.i += 1
    #     # size = 100 - self.i
    #     #size = random.randint(1, 19)
    #     #session = random.randint(-1, 1)
    #     #return Request(self.i, size, "others")
    #     #return SessionReq(self.i, size, session, "others")

    '''TODO: Handle subrequest'''


    # for the structure arrival_time;;;start_time;;;user_id;;;end_time;;;request
    def readNextReq ( self,reqType=None ) :
        nextLine = self.file.readline ( )

        # print(nextLine)
        if nextLine == None :
            return nextLine
        line = str.split ( nextLine, ";;;" )
        if len ( line ) < 2 :
            return None
        startTime = line [ 0 ]
        user = line [ 2 ]
        subreq = str.split ( line [ 4 ], ";" )
        # print(nextLine, "  ", line[4], "  ", len(subreq))
        # print("nextLine: ",nextLine," subReq: ",subreq)
        reqsize = len ( subreq [ 1 ] )
        details = [ subreq [ 0 ], subreq [ 1 ] ]
        if reqType=="BlockDevice":
            details.extend([subreq[2].strip()])
        # elif subreq[0] in ["HOME_TIMELINE","USER_TIMELINE"]:
        elif reqType=="DeathStarSocialMedia": #this is default for tracescaler
            subreq[-1]=subreq[-1].strip()
            details=[x for x in subreq]
        # print("details: ",details,"\n=====================")
        r = Request ( startTime, user, reqsize, details,reqType )
        return r


    def finish ( self ) :
        ''' flush and close file'''
        self.file.close ( )
        print ( "Close readers" )


class TraceReaderNewStructure ( TraceReader ) : #maybe discard this
    '''TODO: Handle subrequest'''


    def readNextReq ( self ) :
        nextLine = self.file.readline ( )

        # print(nextLine)
        if nextLine == None :
            return nextLine
        line = str.split ( nextLine, ";;;" )
        if len ( line ) < 2 :
            return None
        startTime = line [ 0 ]
        user = line [ 2 ]
        subreq = str.split ( line [ 4 ], ";" )
        # print(nextLine, "  ", line[4], "  ", len(subreq))

        reqsize = len ( subreq [ 1 ] )

        details = [ subreq [ 0 ], subreq [ 1 ] ]
        #if reqType == "DeathStarSocialMedia":
        if subreq [ 0 ] in [ "HOME_TIMELINE", "USER_TIMELINE" ]:
            subreq [ -1 ] = subreq [ -1 ].strip ( )
            details = [ x for x in subreq ]
        # if trace_type=="block":
        #     details.extend([subreq[2]])
        r = Request ( startTime, user, reqsize, details )
        return r
    # self.i += 1
    # size = 100 - self.i
    # size = random.randint(1, 19)
    # session = random.randint(-1, 1)
    # return Request(self.i, size, "others")
    # return SessionReq(self.i, size, session, "others")


class TraceWriter ( ABC ) :

    def __init__ ( self, filename ) :
        self.filename = filename
        self.file = open ( self.filename, "w" )
        ''''TODO: open file'''
        print ( "OPEN W", filename )
        return


    '''TODO: Handle subrequest'''


    def writeNextReq ( self, req ) :
        self.file.write ( req.getOutputString ( ) + "\n" )
        '''TODO: write something here'''


    # print(req.timestamp, req.reqSize, req.details)

    def finish ( self ) :
        self.file.close ( )
        '''TODO: flush and close file'''
        print ( "Close writer" )
