package org.example;

import com.google.gson.Gson;
import com.google.gson.JsonObject;


import java.io.Serializable;
import java.util.*;
import java.util.stream.Collectors;

/**
 * Entity class for each traceline
 */
public class TraceLine implements Serializable {

    private int lineNumber;
    private long initialStartTime, actualStartTime;
    private int userNumber;


    private ArrayList< Request > reqList;


    private int currentReqIdx;
    private long currentReqStartTime;

    private long endTime;
    private String reqSizeMappingString;

    public TraceLine ( ) {

        this.reqList = new ArrayList<> ( );


    }









    public void setEndTime ( long endTime ) {
        this.endTime = endTime;
    }



    public long getInitialStartTime ( ) {
        return initialStartTime;
    }

    public void setInitialStartTime ( long initialStartTime ) {
        this.initialStartTime = initialStartTime;
    }

    public void setUserNumber ( int userNumber ) {
        this.userNumber = userNumber;
    }

    public void setCurrentReqIdx ( int currentReqIdx ) {
        this.currentReqIdx = currentReqIdx;
    }


    public void setCurrentReqStartTime ( long currentReqStartTime ) {
        this.currentReqStartTime = currentReqStartTime;
    }

    /**
     * @param s= content of one line of tracefile ie a traceline content
     */

    public void loadFromString ( String s ) {


        String[] traceLine = s.split ( ";;;" );


        this.setInitialStartTime ( Long.parseLong ( traceLine[ 0 ] ) );
        this.setCurrentReqStartTime ( Long.parseLong ( traceLine[ 0 ] ) );

        this.setUserNumber ( Integer.parseInt ( traceLine[ 2 ] ) );
        this.setEndTime ( Long.parseLong ( traceLine[ 3 ] ) );
        this.setCurrentReqIdx ( 0 );


        String[] requestList = traceLine[ 4 ].split ( ";;" );

        //todo: make an if-else block to handle different request types
        //Format of each Request: requestType + ";" + parameter + ";" + thinkTime

        for ( String value : requestList ) {
            String[] request = value.split ( ";" );

            //fixme: the WebRequest class is specific for server. Need to generalize it to Request using the Request interface
            String requestString = request[ 0 ];
//			System.out.println ( "value: " + value );
            try {
                if ( requestString.equalsIgnoreCase ( "READ" ) || requestString.equalsIgnoreCase ( "WRITE" ) ) {

                    BlockDeviceRequest blockDeviceRequest = new BlockDeviceRequest ( RequestType.valueOf ( requestString ), Long.parseLong ( request[ 2 ] ), Integer.parseInt ( request[ 1 ] ) );

                    this.reqList.add ( blockDeviceRequest );

                } else if ( requestString.equalsIgnoreCase ( "HOME_TIMELINE" ) || requestString.equalsIgnoreCase ( "USER_TIMELINE" ) ) {

                    DStarSocMedRequest dStarSocMedRequest = new DStarSocMedRequest ( RequestType.valueOf ( requestString ), Integer.parseInt ( request[ 1 ] ), Integer.parseInt ( request[ 2 ] ), Integer.parseInt ( request[ 3 ] ), Boolean.parseBoolean ( request[ 4 ] ) );

                    this.reqList.add ( dStarSocMedRequest );

                } else {

                    WebRequest r = new WebRequest ( RequestType.valueOf ( requestString ), request[ 1 ], Long.parseLong ( request[ 2 ] ) );

                    this.reqList.add ( r );
                }
            } catch ( NumberFormatException e ) {
                System.out.println ( "trace entry: " + value );

            }

        }


    }

    /**
     * @param traceLines = priority queue of tracelines, from where tracelines would be drawn
     * @param endTime    = endtime of the request that has been executed
     *                   <p>
     *                   This function performs necessary works when a request is done executing:
     *                   1. new traceline to be added to the priority queue
     *                   OR
     *                   2. setting of endtime for this traceline if this traceline is complete
     */



    public String writeFormat ( ) {

        String str = this.initialStartTime + ";;;" + this.actualStartTime + ";;;" + this.userNumber + ";;;" + this.endTime + ";;;";
        StringBuilder str2 = new StringBuilder ( );

        for ( Request request : reqList ) {

            str2.append ( request.writeFormat ( ) ).append ( ";;" );

        }

        str2 = new StringBuilder ( str2.substring ( 0, str2.length ( ) - 2 ) );

        return str + str2;

    }




}
