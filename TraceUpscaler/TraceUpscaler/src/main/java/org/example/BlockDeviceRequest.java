package org.example;

import java.io.Serializable;

public class BlockDeviceRequest implements Request, Serializable {
	
	
	private long offsetInBytes;
	private int payloadSizeInBytes; //payload would read size or write size based on the operation
	private RequestType requestType;
	
	public int getPayloadSizeInBytes ( ) {
		return payloadSizeInBytes;
	}
	
	private String parameter;

	public BlockDeviceRequest ( RequestType requestType, long offsetInBytes, int payloadSizeInBytes ) {
		this.offsetInBytes = offsetInBytes;
		this.payloadSizeInBytes = payloadSizeInBytes;
		this.requestType = requestType;
	}
	
	@Override
	public RequestType getRequestType ( ) {
		return this.requestType;
	}
	
	@Override
	public String writeFormat ( ) {
		
		return this.requestType + ";" + this.payloadSizeInBytes + ";" + this.offsetInBytes;
	}
	
	@Override
	public long getThinkTime ( ) {
		return 0;
	}
	
	@Override
	public String getParameter ( ) {
		return this.parameter;
	}

	public long getOffsetInBytes ( ) {
		return offsetInBytes;
	}
	
	public void setOffsetInBytes ( long offsetInBytes ) {
		this.offsetInBytes = offsetInBytes;
	}
	
	@Override
	public String toString ( ) {
		return "BlockDeviceRequest{" +
				"offset=" + offsetInBytes +
				", payloadSize=" + payloadSizeInBytes +
				", requestType=" + requestType +
				'}';
	}
}

