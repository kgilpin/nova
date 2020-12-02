/*
 * Created on Apr 23, 2003
 */
package nova.applet;

/**
 * Thread which coordinates the starting and stopping of operations.
 * This thread will normally not be running. However, it will be used to make
 * sure that the previous Operation terminates before the next one starts, without interfering
 * with the system event queue thread.
 * 
 * @author gilpin
 */
public class OperationThread 
	extends Thread
{
	private final GUI gui;
	
	private Operation currentOperation = null;
	private Operation nextOperation = null;
	private Thread    currentOperationThread = null;
	private boolean   cancel = false;
	private boolean   isRunning = false;

	public OperationThread(GUI gui)
	{
		super("OperationThread");
			
		this.gui = gui;
		setDaemon(true);
	}

	public boolean isRunning()
	{
		return isRunning;
	}

	public synchronized void beginOperation(Operation op)
	{
		nextOperation = op;
		notifyAll();
	}

	public synchronized void cancel()
	{
		cancel = true;
		nextOperation = null;
		notifyAll();
	}

	public synchronized void operationComplete()
	{
		notifyAll();
	}

	public void run()
	{
		while ( true )
		{
			synchronized ( this )
			{
				try {
					wait();
				}
				catch (InterruptedException x) {
				}
				nextOperation();
			}
		}
	}

	// synchronized from run()
	private void nextOperation()
	{
		if ( ( nextOperation != null || cancel ) &&
			 currentOperation != null )
		{
			currentOperation.cancel();
			try {
				wait();
			}
			catch (InterruptedException x) {
			}
		}
		if ( currentOperation != null )
		{
			currentOperation.postOperation();
		}
		isRunning = false;
		currentOperation = null;
		currentOperationThread = null;
		cancel = false;
		gui.enableControls();
		if ( nextOperation != null )
		{
			gui.disableControls();
			currentOperation = nextOperation;
			nextOperation = null;
			currentOperationThread = new Thread(currentOperation);
			currentOperationThread.start();
			isRunning = true;
		}
	}
	
	interface GUI
	{
		public void enableControls();
		
		public void disableControls();
	}
}
