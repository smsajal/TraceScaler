package org.example;

public interface Request {
	
	public abstract RequestType getRequestType ( );
	
	abstract public String writeFormat ( );
	
	abstract public long getThinkTime ( );
	
	public abstract String getParameter ( );

}
