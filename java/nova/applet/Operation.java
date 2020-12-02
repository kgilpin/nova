/*
 * Created on Apr 23, 2003
 */
package nova.applet;

/**
 * Abstract representation of a dynamic GUI operation, such as an animation.
 * 
 * @author gilpin
 */
public abstract class Operation
	implements Runnable
{
	protected boolean cancel = false;

	public abstract void run();
		
	public void cancel()
	{
		cancel = true;
	}

	public void postOperation()
	{
	}
}
