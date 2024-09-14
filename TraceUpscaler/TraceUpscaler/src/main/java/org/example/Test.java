package org.example;

public class Test {
    public static void main ( String[] args ) {
        String sourceTracePath="";
        String destTracePath="";

        float scalingFactor=0f;

        new TraceUpscalerRunner ().upscale ( sourceTracePath,scalingFactor,destTracePath );
    }
}
