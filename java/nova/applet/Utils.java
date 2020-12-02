/*
 * Created on Jun 6, 2003
 */
package nova.applet;

/**
 * @author gilpin
 */
public class Utils
{
	public static Double toDouble(String str)
	{
		if ( str == null || "".equals(str) )
		{
			return null;
		}
		else
		{
			try
			{
				return Double.valueOf(str);
			}
			catch (NumberFormatException x)
			{
				System.out.println("Can't convert " + str + " to Double");
				return null;
			}
		}
	}

	public static Integer toInteger(String str)
	{
		if ( str == null || "".equals(str) )
		{
			return null;
		}
		else
		{
			try
			{
				return Integer.valueOf(str);
			}
			catch (NumberFormatException x)
			{
				System.out.println("Can't convert " + str + " to Integer");
				return null;
			}
		}
	}
}
