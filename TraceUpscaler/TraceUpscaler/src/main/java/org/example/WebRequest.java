package org.example;


import java.io.Serializable;

public class WebRequest implements Request, Serializable {

    private RequestType requestType;
    private String parameter;

    private long thinkTime;


    public WebRequest ( RequestType requestType, String parameter, long thinkTime ) {
        this.requestType = requestType;
        this.parameter = parameter;
        this.thinkTime = thinkTime;
    }

    @Override
    public long getThinkTime ( ) {
        return thinkTime;
    }



    @Override
    public RequestType getRequestType ( ) {
        return requestType;
    }



    @Override
    public String getParameter ( ) {
        return parameter;
    }



    @Override
    public String writeFormat ( ) {
        /**
         * actual parameter is not printed anymore to avoid problem with large payloads
         * */
        return requestType + ";" + parameter + ";" + thinkTime;
    }

    @Override
    public String toString ( ) {
        return "WebRequest{" +
                "requestType=" + requestType +
                ", parameter='" + parameter + '\'' +
                ", thinkTime=" + thinkTime +
                '}';
    }
}

