package test;

import org.apache.xmlrpc.XmlRpc;
import org.apache.xmlrpc.XmlRpcClient;
import org.apache.xmlrpc.XmlRpcException;

import java.applet.Applet;
import java.awt.*;
import java.awt.event.*;
import java.io.IOException;
import java.net.URL;
import java.net.MalformedURLException;
import java.util.Hashtable;
import java.util.Vector;

public class APIApplet
   extends Applet
{
	static
	{
		XmlRpc.debug = true;
		// MSIE does not support ISO8859_1, which is the XmlRpc default
		XmlRpc.setEncoding("UTF8");
	}

	public APIApplet()
	{
		Button button = new Button("DispatchFleet");
		button.addActionListener(new ActionListener()
			{
				public void actionPerformed(ActionEvent e)
				{
					dispatchFleet(12, "newgame-kevin", "kevin", "star9", "star11", 1);
				}
			});
		add(button);
	}

	public String dispatchFleet(int gameID, String playerName, String password, String origin,
										  String destination, int numShips)
	{
		checkNull(playerName, "playerName");
		checkNull(password, "password");
		checkNull(origin, "origin");
		checkNull(destination, "destination");

		try 
		{
			URL codeBase = getDocumentBase();
			URL rpcServerURL = new URL(codeBase, "/nova/XMLRPCAPI.py");
			XmlRpcClient xmlrpc = new XmlRpcClient(rpcServerURL);
			Vector params = new Vector ();
			params.addElement( new Integer(gameID) );
			params.addElement( playerName );
			params.addElement( password );
			params.addElement( origin );
			params.addElement( destination );
			params.addElement( new Integer(numShips) );
						
			Hashtable result = (Hashtable)xmlrpc.execute ("dispatchFleet", params);

			System.out.println(result);

			Integer code = (Integer)result.get("succeeded");
			if ( code.intValue() == 0 )
				 return null;
			else
				 return String.valueOf(result.get("errorMessage"));
				 
		}
		catch (MalformedURLException x)
		{
			x.printStackTrace();
		}
		catch (XmlRpcException x)
		{
			x.printStackTrace();
		}
		catch (IOException x)
		{
			x.printStackTrace();
		}
		return "Unexpected exception";
	}

	private void checkNull(Object value, String argumentName)
	{
		if ( value == null )
			throw new RuntimeException("Argument '" + argumentName + "' is null in APIApplet");
	}
}
