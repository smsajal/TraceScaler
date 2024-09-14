package org.example;


import org.apache.commons.lang3.SerializationUtils;
import org.apache.commons.math3.random.RandomDataGenerator;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;

public class TraceUpscaler {

    public List< Long > getNewArrivalTimes ( List< Long > oldArrivalTimes, float upscalingFactor ) {


        List< Long > newArrivalTimes = new ArrayList<> ( );
        int requiredSize = oldArrivalTimes.size ( );
        int whole = ( int ) ( Math.floor ( upscalingFactor ) );
        double fraction = upscalingFactor - whole;


        for ( Long x : oldArrivalTimes
        ) {


            int newRequestCount = whole;
            if ( new RandomDataGenerator ( ).nextUniform ( 0, 1 ) < fraction ) {
                newRequestCount++;

            }
            List< Long > samples = new ArrayList<> ( Collections.nCopies ( newRequestCount, x ) );


            newArrivalTimes.addAll ( samples );

            if ( newArrivalTimes.size ( ) >= requiredSize ) {
                break;
            }
        }


        newArrivalTimes = newArrivalTimes.subList ( 0, requiredSize );

        return newArrivalTimes;
    }

    public ArrayList< TraceLine > upscaleTrace ( ArrayList< TraceLine > traceLines, float upscalingFactor ) {


        List< Long > initialStartTimes = traceLines.stream ( ).map ( TraceLine :: getInitialStartTime ).collect ( Collectors.toList ( ) );

        List< Long > newInitialStartTimes = this.getNewArrivalTimes ( initialStartTimes, upscalingFactor );

        int i = 0;
        ArrayList< TraceLine > newTraceLines = new ArrayList<> ( );
        for ( TraceLine x : traceLines
        ) {
            newTraceLines.add ( SerializationUtils.clone ( x ) );
            TraceLine y = newTraceLines.get ( newTraceLines.size ( ) - 1 );
            y.setInitialStartTime ( newInitialStartTimes.get ( i ) );
            i++;
        }


        return newTraceLines;
    }
}
