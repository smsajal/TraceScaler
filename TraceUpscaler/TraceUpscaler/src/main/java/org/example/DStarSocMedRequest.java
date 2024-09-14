package org.example;

import java.io.Serializable;

public class DStarSocMedRequest implements Request, Serializable {

    private RequestType requestType;
    private int userId;
    private int timelineStart, timelineStop;
    private boolean isCacheHit = false;


    public DStarSocMedRequest ( RequestType requestType, int userId, int timelineStart, int timelineStop, boolean isCacheHit ) {
        this.requestType = requestType;
        this.userId = userId;
        this.timelineStart = timelineStart;
        this.timelineStop = timelineStop;
        this.isCacheHit = isCacheHit;
    }

    @Override
    public RequestType getRequestType ( ) {
        return this.requestType;
    }

    public void setRequestType ( RequestType requestType ) {
        this.requestType = requestType;
    }

    @Override
    public String writeFormat ( ) {
        return this.requestType + ";" + this.userId + ";" + this.timelineStart + ";" + this.timelineStop + ";" + this.isCacheHit;
    }

    @Override
    public long getThinkTime ( ) {
        return 0;
    }

    @Override
    public String getParameter ( ) {
        return null;
    }


    public int getPayloadSize ( ) {
        return 0;
    }

    @Override
    public String toString ( ) {
        return "DStarSocMedRequest{" +
                "requestType=" + requestType +
                ", userId=" + userId +
                ", timelineStart=" + timelineStart +
                ", timelineStop=" + timelineStop +
                ", isCacheHit=" + isCacheHit +
                '}';
    }

    public String getUrlExtension ( ) {

        String urlExtenstion = "";
        switch ( this.requestType ) {
            case HOME_TIMELINE -> urlExtenstion = "home-timeline";
            case USER_TIMELINE -> urlExtenstion = "user-timeline";
            default ->
                    throw new IllegalArgumentException ( "DStarSocMedRequest does not support requestType: " + this.requestType );
        }

        urlExtenstion += "/read?user_id=" + this.userId + "&start=" + this.timelineStart + "&stop=" + this.timelineStop;

        return urlExtenstion;
    }

    public int getUserId ( ) {
        return userId;
    }

    public void setUserId ( int userId ) {
        this.userId = userId;
    }

    public int getTimelineStart ( ) {
        return timelineStart;
    }

    public void setTimelineStart ( int timelineStart ) {
        this.timelineStart = timelineStart;
    }

    public int getTimelineStop ( ) {
        return timelineStop;
    }

    public void setTimelineStop ( int timelineStop ) {
        this.timelineStop = timelineStop;
    }

    public boolean isCacheHit ( ) {
        return isCacheHit;
    }

    public void setCacheHit ( boolean cacheHit ) {
        isCacheHit = cacheHit;
    }
}
