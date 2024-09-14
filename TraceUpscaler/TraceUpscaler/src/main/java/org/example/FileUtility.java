package org.example;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;


import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class FileUtility {


    public JsonObject readJsonObject ( String jsonFilePath ) {

        JsonObject jsonObject = null;
        JsonParser jsonParser = new JsonParser ( );

        try {

            FileReader fileReader = new FileReader ( jsonFilePath );
            Object object = jsonParser.parse ( fileReader );
            jsonObject = ( JsonObject ) object;
            fileReader.close ( );

        } catch ( IOException e ) {
            e.printStackTrace ( );
        }
        return jsonObject;
    }

    public ArrayList< TraceLine > readTraceLines ( String traceFileAddress ) {

        List< TraceLine > temp = new ArrayList<> ( );
        try ( Stream< String > stream = Files.lines ( Paths.get ( traceFileAddress ) ) ) {
            temp = stream.map ( FileUtility :: getTraceLineFromTraceString ).collect ( Collectors.toList ( ) );
        } catch ( IOException e ) {
            e.printStackTrace ( );
        }

        return new ArrayList<> ( temp );
    }
    public static TraceLine getTraceLineFromTraceString ( String traceString ) {
        TraceLine traceLine = new TraceLine ( );
        traceLine.loadFromString ( traceString );
        return traceLine;
    }

    public void writeTraceLines ( String fileName, ArrayList< TraceLine > traceLines ) {

        try {
            BufferedWriter bufferedWriter = new BufferedWriter ( new FileWriter ( fileName ) );
            for ( TraceLine traceLine : traceLines ) {
                bufferedWriter.write ( traceLine.writeFormat ( ) + "\n" );

            }
            bufferedWriter.close ( );

        } catch ( IOException e ) {
            e.printStackTrace ( );
        }

    }
}
































