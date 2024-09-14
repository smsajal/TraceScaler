package org.example;

import java.util.ArrayList
        ;

public class TraceUpscalerRunner {

    FileUtility fileUtility;
    TraceUpscaler traceUpscaler;
    public TraceUpscalerRunner ( ) {

        this.fileUtility=new FileUtility ();
        this.traceUpscaler=new TraceUpscaler ();
    }

    public void upscale( String sourceTracePath, float scalingFactor, String destTracePath){


        ArrayList<TraceLine> inputTrace=this.fileUtility.readTraceLines ( sourceTracePath );

        ArrayList<TraceLine> upscaledTrace=this.traceUpscaler.upscaleTrace ( inputTrace,scalingFactor ) ;

        this.fileUtility.writeTraceLines ( destTracePath,upscaledTrace );



    }

    public static void main ( String[] args ) {
        String sourceTracePath=args[0];
        String destTracePath=args[1];
        float scalingFactor=Float.parseFloat ( args[2] );

        new TraceUpscalerRunner ().upscale ( sourceTracePath,scalingFactor,destTracePath );
    }
}
