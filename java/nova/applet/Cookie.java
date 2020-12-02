/*
 * Created on Jun 6, 2003
 */
package nova.applet;

import java.applet.Applet;
import java.text.SimpleDateFormat;
import java.util.Calendar;

import netscape.javascript.JSObject;

/**
 * @author gilpin
 * @see http://www.devguru.com/Technologies/ecmascript/quickref/doc_cookie.html
 * @see http://www.rgagnon.com/javadetails/java-0180.html
 */
public class Cookie
{
	// Cookie spec wants : Wdy, DD-Mon-YYYY HH:MM:SS GMT
	private static final SimpleDateFormat SDF = new SimpleDateFormat("EEE, dd-MMM-yyyy HH:mm:ss 'GMT'");
	
	public static final int EXPIRE_SESSION = 0;
	public static final int EXPIRE_NEVER = 1;
	
	/**
	 * Set a named cookie value. No optional parameters such as expiration date
	 * are specified.
	 */
	public static void setCookie(Applet applet, String name, String value, int expire) 
	{
		String cookieStr = name + "=" + value;
		if ( expire == EXPIRE_NEVER )
		{
			Calendar c = Calendar.getInstance();
			c.add(java.util.Calendar.YEAR, 10);
			cookieStr += "; expires=" + SDF.format(c.getTime());
		}
		JSObject browser = JSObject.getWindow(applet);
		JSObject document = (JSObject)browser.getMember("document");
		// System.out.println("Setting cookie = " + cookieStr);
		document.setMember("cookie", cookieStr);
	}
	
	/**
	 * Get a specific cookie by its name, parsing the cookie string.
	 */
	public static String getCookie(Applet applet, String name)
	{
		String cookie = getCookies(applet);
		// System.out.println("Looking for cookie " + name + " in " + cookie);
		String search = name + "=";
		if (cookie.length() > 0)
		{
			int offset = cookie.indexOf(search);
			if (offset != -1)
			{
				offset += search.length();
				int end = cookie.indexOf(";", offset);
				if (end == -1)
					end = cookie.length();
				return cookie.substring(offset, end);
			}
		}
		return "";
	}
       
	/**
	 * Get all cookies for a document
	 */
	private static String getCookies(Applet applet) 
	{
		try
		{
			JSObject browser = (JSObject)JSObject.getWindow(applet);
			JSObject document = (JSObject)browser.getMember("document");
			String cookie = (String)document.getMember("cookie");
			if (cookie.length() > 0)
				return cookie;
		}
		catch (Exception e)
		{
			e.printStackTrace();
		}
		return "";
	}
}
