package nova.applet;

// Good site on Java-JavaScript : http://www.rgagnon.com/masters/java-js.html
import netscape.javascript.JSObject;

import java.applet.Applet;
import java.awt.*;
import java.awt.event.*;
import java.text.DecimalFormat;
import java.util.Hashtable;
import java.util.Vector;

public class NovaApplet 
	extends Applet
	implements OperationThread.GUI
{
	public static final int BORDER_PARSECS = 5;
	public static Font DEFAULT_FONT;
	public static Font BOLD_FONT;

	public static final Color DARK_GRAY = new Color(100, 100, 100);
	public static final Color UNOWNED_STAR_COLOR = new Color(170, 170, 170);
	public static final Color VERY_LIGHT_GRAY = new Color(200, 200, 200);
	public static final Color WHITE = Color.white;
	public static final Color BLUE = Color.blue;
	public static final Color GREEN = new Color(0, 160, 0);
	public static final Color RED = new Color(150, 0, 0);

	// TODO: the cookies should be parameterized by gameID so that settings from
	// different games can co-exist
	private static final String CENTER_X_COOKIE = "AppletCenterX";
	private static final String CENTER_Y_COOKIE = "AppletCenterY";
	private static final String ZOOM_COOKIE = "AppletZoom";

	private static final Color PROBE_COLOR = GREEN;
	private static final Color BOMB_COLOR = RED;
	private static final Color FLEET_COLOR = BLUE;

	private static final int LEGEND_BORDER = 2;
	private static final int SCROLL_INCREMENT = 3;
	private static final int STAR_RADIUS = 3;
	private static final int FLEET_OVAL_RADIUS = 4;
	private static final int DASH_LENGTH = 5;

	private static final double DEFAULT_PARSEC_PIXELS = 5;

	private static final int NUM_PLAYERS = 13;
	private static final char SEPARATOR_CHAR = '|';
	private static final char ESCAPE_CHAR = '\\';

	private final Object REPAINT_MONITOR = new Object();
	private final OperationThread operationThread = new OperationThread(this);
	private final Vector playerColors = new Vector();
	private final Hashtable playerColorsByPlayer = new Hashtable();
	private final MouseTracker mouseTracker = new MouseTracker();
	private final Legend legend = new Legend();
	private final Legend commands = new Legend();

	private boolean showFleets = true, showInfo = true, showNames = true;
	private boolean debug = false;

	private Star[] stars;
	private Fleet[] fleets;
	private double range;	// player's range
	private String player;	// player's name
	private Color thisPlayerColor;
	
	// The zoom factor
	private double zoom = 1.0f;
	// The X and Y coordinates of the center of the map, in parsecs
	private int centerX, centerY;

	private int selectionAnimationFrame = -1;

	Star moveSource = null, moveTarget = null, zoomStar = null;
	Point mousePoint = null;

	//	double-buffer variables
	private int bufferWidth;
	private int bufferHeight;
	private Image bufferImage;
	private Graphics bufferGraphics;

	static {
		System.out.println("Available fonts:");
		String[] fontList = Toolkit.getDefaultToolkit().getFontList();
		for (int i = 0; i < fontList.length; ++i)
			System.out.println(fontList[i]);

		DEFAULT_FONT = Font.decode("SansSerif-PLAIN-11");
		BOLD_FONT = Font.decode("SansSerif-BOLD-11");
		System.out.println("Default font: " + DEFAULT_FONT);
		System.out.println("Bold font: " + BOLD_FONT);
	}

	public NovaApplet()
	{
		System.out.println("NovaApplet constructing");

		centerX = 0;
		centerY = 0;

		// TODO: show commands in lower-left of applet
		commands.add(new Label("'f' : Toggle fleets"));
		commands.add(new Label("'i' : Toggle star info"));
		commands.add(new Label("Commands:"));

		legend.add(new RangeDisplay());
		legend.add(new ProbeIcon(PROBE_COLOR, "Probe"));
		legend.add(new ProbeIcon(BOMB_COLOR, "Nova Bomb"));
		legend.add(new FleetIcon());
		legend.add(new UnownedStarIcon());

		addKeyListener(new KeyAdapter()
		{
			public void keyPressed(KeyEvent event)
			{
				switch (event.getKeyCode())
				{
					case KeyEvent.VK_ESCAPE :
						mouseTracker.cancel();
						break;
					case KeyEvent.VK_UP :
						scroll(0, -SCROLL_INCREMENT);
						break;
					case KeyEvent.VK_DOWN :
						scroll(0, SCROLL_INCREMENT);
						break;
					case KeyEvent.VK_LEFT :
						scroll(-SCROLL_INCREMENT, 0);
						break;
					case KeyEvent.VK_RIGHT :
						scroll(SCROLL_INCREMENT, 0);
						break;
				}
				switch (event.getKeyChar())
				{
					case 'f' :
						showFleets = !showFleets;
						break;
					case 'n' :
						showNames = !showNames;
						break;
					case 'i' :
						showInfo = !showInfo;
						break;
					case '+' :
						zoom(1.5);
						break;
					case '-' :
						zoom(1 / 1.5);
						break;
				}
				repaint();
			}
		});

		addMouseListener(new MouseAdapter()
		{
			public void mouseClicked(MouseEvent event)
			{
				mouseTracker.mouseClicked(event);
			}
		});
		addMouseMotionListener(new MouseMotionAdapter()
		{
			public void mouseMoved(MouseEvent event)
			{
				mouseTracker.mouseMoved(event);
			}
		});
	}

	public void init()
	{
		System.out.println("NovaApplet init-ing");

		setBackground(Color.black);
		allocateColors();

		debug = "true".equals(getParameter("debug"));

		player = getParameter("player");
		range = Double.valueOf(getParameter("range")).doubleValue();

		String playerColorStr = getParameter("playercolor");
		thisPlayerColor =
			new Color(
				Integer.parseInt(playerColorStr.substring(0, 3)),
				Integer.parseInt(playerColorStr.substring(3, 6)),
				Integer.parseInt(playerColorStr.substring(6, 9)));

		Vector starVec = new Vector();
		Vector fleetVec = new Vector();
		for (int i = 0; true; ++i)
		{
			String key = "star" + (i + 1);
			if (getParameter(key) != null)
			{
				Star star = new Star(new ParameterTokenizer(getParameter(key)));
				if (debug)
					System.out.println(star);
				starVec.addElement(star);
			}
			else
			{
				break;
			}
		}

		stars = new Star[starVec.size()];
		starVec.copyInto(stars);

		for (int i = 0; true; ++i)
		{
			String key = "fleet" + (i + 1);
			if (getParameter(key) != null)
			{
				Fleet fleet =
					new Fleet(new ParameterTokenizer(getParameter(key)));
				fleetVec.addElement(fleet);
			}
			else
			{
				break;
			}
		}

		fleets = new Fleet[fleetVec.size()];
		fleetVec.copyInto(fleets);
		
		operationThread.start();
	}

	public void update(Graphics g)
	{
		paint(g);
	}

	/**
	 * Cancel the current {@link Operation}.
	 */
	public void cancel()
	{
		operationThread.cancel();
	}

	/**
	 * No current behavior.
	 */	
	public void enableControls()
	{
	}
	
	/**
	 * No current behavior.
	 */	
	public void disableControls()
	{
	}

	public void zoomToStar(String name)
	{
		Star star = getStar(name);
		operationThread.beginOperation(new SelectStarOperation(star));					
	}

	public void paint(Graphics g)
	{
		synchronized ( REPAINT_MONITOR )
		{
			//	checks the buffersize with the current panelsize
			//	or initializes the image with the first paint
			if (bufferWidth != getSize().width
				|| bufferHeight != getSize().height
				|| bufferImage == null
				|| bufferGraphics == null)
				resetBuffer();
	
			if (bufferGraphics != null)
			{
				//	this clears the offscreen image, not the onscreen one
				bufferGraphics.setColor(Color.black);
				bufferGraphics.clearRect(0, 0, bufferWidth, bufferHeight);
	
				//	calls the paintbuffer method with the offscreen graphics as a param
				paintBuffer(bufferGraphics);
	
				//	we finaly paint the offscreen image onto the onscreen image
				g.drawImage(bufferImage, 0, 0, this);
			}
			
			REPAINT_MONITOR.notifyAll();
		}
	}

	public void paintBuffer(Graphics g)
	{
		for (int i = 0; i < stars.length; ++i)
		{
			stars[i].render(g);
		}
		if (showFleets)
		{
			for (int i = 0; i < fleets.length; ++i)
			{
				fleets[i].render(g);
			}
		}
		legend.render(g);
	}

	public void start()
	{
		System.out.println("NovaApplet starting");
		
		int maxX = 0, maxY = 0;
		for (int i = 0; i < stars.length; ++i)
		{
			Star star = stars[i];
			maxX = (int)Math.max(star.x, maxX);
			maxY = (int)Math.max(star.y, maxY);
		}

		loadProjection(maxX, maxY);
		
		new StoreProjectionThread().start();
	}

	/**
	 * -1 turns the selection animation off
	 */
	void setSelectionAnimationFrame(int frame)
	{
		this.selectionAnimationFrame = frame;
	}

	int getSelectionAnimationRadius()
	{
		if ( selectionAnimationFrame == -1 )
			return -1;
		else
			return (int)( selectionAnimationFrame * DEFAULT_PARSEC_PIXELS / 2.0 );
	}

	public Star pickStar(Point point)
	{
		if (debug)
			System.out.println("Picking star at " + point);

		for (int i = 0; i < stars.length; ++i)
		{
			Star star = stars[i];
			int x = getStarPixelX(star);
			int y = getStarPixelY(star);
			if (debug)
				System.out.println(star.name + " is ( " + x + ", " + y + " )");
			int dx = point.x - x;
			int dy = point.y - y;
			double distance = Math.sqrt(dx * dx + dy * dy);
			if (distance <= STAR_RADIUS)
				return star;
		}
		return null;
	}

	Star getStar(String starName)
	{
		for (int i = 0; i < stars.length; ++i)
			if (stars[i].name.equals(starName))
				return stars[i];
		throw new IllegalArgumentException("Unknown star : " + starName);
	}

	int parsecsToPixels(double parsecs)
	{
		return (int)( parsecs * DEFAULT_PARSEC_PIXELS * zoom ); 
	}

	double pixelsToParsecs(double pixels)
	{
		return pixels / ( DEFAULT_PARSEC_PIXELS * zoom ); 
	}

	int getStarPixelX(Star star)
	{
		return getPixelX(star.x);
	}

	int getStarPixelY(Star star)
	{
		return getPixelY(star.y);
	}

	int getPixelX(double x)
	{
		/*
		 * Compute the difference between x and the center of the display
		 * Scale by pixels and add 1/2 of the screen width
		 */
		 
		int pixelDX = parsecsToPixels(x - centerX);
		return pixelDX + getSize().width / 2;
	}

	int getPixelY(double y)
	{
		int pixelDY = parsecsToPixels(y - centerY);
		return pixelDY + getSize().height / 2;
	}

	Dimension textSize(Graphics g, String text)
	{
		FontMetrics metrics = g.getFontMetrics();
		return new Dimension(metrics.stringWidth(text), metrics.getHeight());
	}

	Dimension fleetOvalSize(Graphics g)
	{
		return new Dimension(
			FLEET_OVAL_RADIUS * 2 + 1,
			FLEET_OVAL_RADIUS * 2 + 1);
	}

	/** x, y are the center of the oval */
	void drawFleetOval(Graphics g, int x, int y, Color color)
	{
		Dimension d = fleetOvalSize(g);
		x -= d.width / 2;
		y -= d.height / 2;
		g.setColor(color);
		g.fillOval(x, y, d.width, d.height);

		// Draw white circle at location
		g.setColor(WHITE);
		g.drawOval(x, y, d.width, d.height);
	}

	Dimension fleetRectSize(Graphics g, int numShips)
	{
		Dimension textSize = textSize(g, String.valueOf(numShips));
		return new Dimension(textSize.width + 2, textSize.height + 1);
	}

	void drawAsterix(Graphics g, int x, int y)
	{
		// Draw an asterix for the star itself
		g.drawLine(x - STAR_RADIUS, y, x + STAR_RADIUS, y);
		g.drawLine(
			x - STAR_RADIUS,
			y - STAR_RADIUS,
			x + STAR_RADIUS,
			y + STAR_RADIUS);
		g.drawLine(x, y - STAR_RADIUS, x, y + STAR_RADIUS);
		g.drawLine(
			x - STAR_RADIUS,
			y + STAR_RADIUS,
			x + STAR_RADIUS,
			y - STAR_RADIUS);
	}

	/** x, y are the x,y location of the rectangle */
	void drawFleetRect(Graphics g, int x, int y, int numShips)
	{
		Dimension d = fleetRectSize(g, numShips);
		x -= d.width / 2;
		y -= d.height / 2;
		g.setColor(FLEET_COLOR);
		g.fillRect(x, y, d.width, d.height);

		// Draw white rectangle at location
		g.setColor(WHITE);
		g.drawRect(x, y, d.width, d.height);

		// Draw white ship description in box
		g.drawString(String.valueOf(numShips), x + 2, y + d.height - 1);
	}

	/**
		* Returns a unique color for the player.
		*/
	synchronized Color getPlayerColor(String player)
	{
		if (player == null)
			player = "";
		Color color;
		if ( player.equals("Nobody") )
		{
			color = UNOWNED_STAR_COLOR;
		}
		else if ( player.equals(this.player) )
		{
			color = thisPlayerColor;
		}
		else
		{
			// System.out.println("Getting color for player " + player);
			color = (Color)playerColorsByPlayer.get(player);
			if (color == null)
			{
				if (!playerColors.isEmpty())
				{
					color = (Color)playerColors.elementAt(0);
					playerColors.removeElementAt(0);
				}
				else
				{
					color =
						new Color(
							(int) (Math.random() * 128) + 127,
							(int) (Math.random() * 128) + 127,
							(int) (Math.random() * 128) + 127);
				}
				playerColorsByPlayer.put(player, color);
			}
		}
		return color;
	}

	private void scroll(int dx, int dy)
	{
		centerX += dx;
		centerY += dy;
	}

	private void zoom(double factor)
	{
		zoom *= factor;
		zoom = Math.max(zoom, 1.0 / DEFAULT_PARSEC_PIXELS);
	}

	private void loadProjection(int width, int height)
	{
		Integer dCenterX = Utils.toInteger(Cookie.getCookie(this, CENTER_X_COOKIE));
		Integer dCenterY = Utils.toInteger(Cookie.getCookie(this, CENTER_Y_COOKIE));
		Double dZoom = Utils.toDouble(Cookie.getCookie(this, ZOOM_COOKIE));
	
		if ( dCenterX == null || dCenterY == null )
		{			
			centerX = width / 2;
			centerY = height / 2;
		}
		else
		{
			centerX = dCenterX.intValue();
			centerY = dCenterY.intValue();
		}

		if ( dZoom == null )
		{		
			// Compute the initial zoom factor so that the stars will all fit in the display 
			double zoomX = getSize().width / ( ( width + BORDER_PARSECS * 2 ) * DEFAULT_PARSEC_PIXELS );
			double zoomY = getSize().height / ( ( height + BORDER_PARSECS * 2 ) * DEFAULT_PARSEC_PIXELS );
			zoom = Math.min(zoomX, zoomY);
		}
		else
		{
			zoom = dZoom.doubleValue();
		}
	}

	private void allocateColors()
	{
		playerColors.addElement(new Color(204, 204, 204));
		playerColors.addElement(new Color(255, 255, 51));
		playerColors.addElement(new Color(255, 153, 255));
		playerColors.addElement(new Color(255, 153, 0));
		playerColors.addElement(new Color(0, 255, 153));
		playerColors.addElement(new Color(236, 224, 155));
		playerColors.addElement(new Color(255, 136, 136));
		playerColors.addElement(new Color(255, 51, 51));
		playerColors.addElement(new Color(0, 255, 255));
		playerColors.addElement(new Color(255, 69, 193));
		playerColors.addElement(new Color(255, 102, 51));
		playerColors.addElement(new Color(153, 109, 255));
		playerColors.addElement(new Color(0, 153, 255));
	}

	private void resetBuffer()
	{
		// always keep track of the image size
		bufferWidth = getSize().width;
		bufferHeight = getSize().height;

		//	clean up the previous image
		if (bufferGraphics != null)
		{
			bufferGraphics.dispose();
			bufferGraphics = null;
		}
		if (bufferImage != null)
		{
			bufferImage.flush();
			bufferImage = null;
		}
		System.gc();

		//	create the new image with the size of the panel
		bufferImage = createImage(bufferWidth, bufferHeight);
		bufferGraphics = bufferImage.getGraphics();
	}

	private void synchronizedRepaint()
	{
		synchronized ( REPAINT_MONITOR )
		{
			repaint();
			try {
				// Wait for the notifyAll in #paint
				// This ensures that each scene is rendered before the next one is received.
				// System.out.println("renderClientData#wait");
				REPAINT_MONITOR.wait();
			}
			catch (InterruptedException x) {
			}
		}
	}

	/**
	 * Keeps the projection parameters in synch with the browser cookies. Every 1/4
	 * second it checks to see if they have changed
	 */
	private class StoreProjectionThread
		extends Thread
	{
		int centerX;
		int centerY;
		double zoom;
		
		public StoreProjectionThread()
		{
			setDaemon(true);
			update();
		}
		
		public void run()
		{
			while ( true )
			{
				if ( this.centerX != NovaApplet.this.centerX ||
						this.centerY != NovaApplet.this.centerY ||
						this.zoom != NovaApplet.this.zoom )
				{				
					// System.out.println("Updating projection cookies");
					update();
					Cookie.setCookie(NovaApplet.this, CENTER_X_COOKIE, String.valueOf(centerX), Cookie.EXPIRE_NEVER);
					Cookie.setCookie(NovaApplet.this, CENTER_Y_COOKIE, String.valueOf(centerY), Cookie.EXPIRE_NEVER);
					Cookie.setCookie(NovaApplet.this, ZOOM_COOKIE, String.valueOf(zoom), Cookie.EXPIRE_NEVER);
				}
				try
				{
					Thread.sleep(1000);
				}
				catch (InterruptedException e)
				{
				}	
			}
		}
		
		private void update()
		{
			this.centerX = NovaApplet.this.centerX;
			this.centerY = NovaApplet.this.centerY;
			this.zoom = NovaApplet.this.zoom;
		}
	}

	/**
	 * Animates the selection of a star by drawing converging circles
	 * around it.
	 */
	class SelectStarOperation
		extends Operation
	{
		private final Star star;
		
		public SelectStarOperation(Star star)
		{
			this.star = star;
		}
		
		public void run()
		{
			zoomStar = star; 
			try {
				for ( int i = 8; !cancel && i >= -1; --i )
				{
					setSelectionAnimationFrame(i);
					long startTime = System.currentTimeMillis();
					synchronizedRepaint();
					long delta = System.currentTimeMillis() - startTime;
					if ( delta < 125 )
					{
						try
						{
							Thread.sleep(125 - delta);
						}
						catch (InterruptedException x)
						{
						}
					}
				}
			}
			finally {
				zoomStar = null;
				operationThread.operationComplete();
			}
		}
	}

	class MouseTracker
	{
		public void cancel()
		{
			if (moveSource != null)
			{
				moveSource = null;
				repaint();
			}
		}

		public void mouseClicked(MouseEvent event)
		{
			Star star = pickStar(event.getPoint());
			if (star != null && star != moveSource)
			{
				if (debug)
					System.out.println("Clicked on " + star.name);
				if (moveSource == null)
				{
					if (debug)
						System.out.println("\tSetting moveSource");
					moveSource = star;
				}
				else if (moveSource.owner.equals(player) && !star.isDead)
				{
					if (debug)
						System.out.println(
							"\tOpening dispatch window from "
								+ moveSource.name
								+ " to "
								+ star.name);
					JSObject js = JSObject.getWindow(NovaApplet.this);
					js.call(
						"dispatch",
						new String[] { moveSource.name, star.name });
					// Other stuff you can do with JSObject
					// js.eval("alert('" + star.name + "')");
					moveSource = null;
				}
			}
			else
			{
				moveSource = null;
			}
			repaint();
		}

		public void mouseMoved(MouseEvent event)
		{
			mousePoint = event.getPoint();

			if (debug)
				System.out.println(mousePoint);

			boolean repaint = false;
			if (moveSource != null)
			{
				repaint = true;
			}

			Star star = pickStar(event.getPoint());
			if (star != null)
			{
				moveTarget = star;
				repaint = true;
			}
			else if (moveTarget != null)
			{
				repaint = true;
				moveTarget = null;
			}

			if (repaint)
				repaint();
		}
	}

	/*
	 * The legend is drawn in the lower-right of the screen. It consists of a list of LegendItems,
	 * each of which renders itself in the legend area. The legend background is black and is drawn
	 * with a white border.
	 */
	class Legend
	{
		Vector items = new Vector();

		public void add(LegendItem item)
		{
			items.addElement(item);
		}

		public void render(Graphics g)
		{
			int height = 0, width = 0;
			for (int i = 0; i < items.size(); ++i)
			{
				LegendItem item = (LegendItem)items.elementAt(i);
				Dimension d = item.size(g);
				width = (int)Math.max(width, d.width + 2 * LEGEND_BORDER);
				height += d.height + 2 * LEGEND_BORDER;
			}

			int bottom = getSize().height;
			int top = getSize().height - height;
			int right = getSize().width;
			g.setColor(Color.black);
			g.fillRect(right - width, top, width, height);

			g.setColor(Color.white);
			g.drawRect(right - width, top, width, height);

			int x = right - width + LEGEND_BORDER, y = bottom - LEGEND_BORDER;
			for (int i = 0; i < items.size(); ++i)
			{
				LegendItem item = (LegendItem)items.elementAt(i);
				item.render(g, new Point(x, y));
				y -= item.size(g).height + LEGEND_BORDER * 2;
			}
		}
	}

	/**
	 * An item which is contained in the Legend. The legend automatically sizes and renders itself
	 * according to the implementation of the methods in this interface.
	 */
	interface LegendItem
	{
		public Dimension size(Graphics g);

		public void render(Graphics g, Point point);
	}

	class Label implements LegendItem
	{
		private final String text;
		
		public Label(String text)
		{
			this.text = text;
		}

		public Dimension size(Graphics g)
		{
			return textSize(g, text);
		}

		public void render(Graphics g, Point point)
		{
			g.drawString(text, point.x, point.y);			
		}		
	}

	class ProbeIcon implements LegendItem
	{
		private final Color color;
		private final String text;

		public ProbeIcon(Color color, String text)
		{
			this.color = color;
			this.text = "  " + text;
		}

		public Dimension size(Graphics g)
		{
			Dimension fleetOvalSize = fleetOvalSize(g);
			Dimension textSize = textSize(g, text);
			return new Dimension(
				fleetOvalSize.width + 2 + textSize.width,
				(int)Math.max(fleetOvalSize.height, textSize.height));
		}

		public void render(Graphics g, Point point)
		{
			Dimension fleetOvalSize = fleetOvalSize(g);
			drawFleetOval(
				g,
				point.x + fleetOvalSize.width / 2,
				point.y - fleetOvalSize.height / 2,
				color);
			g.drawString(text, point.x + fleetOvalSize.width + 2, point.y);
		}
	}

	class FleetIcon implements LegendItem
	{
		private final int numShips = 10;

		public Dimension size(Graphics g)
		{
			Dimension fleetRectSize = fleetRectSize(g, numShips);
			Dimension textSize = textSize(g, "  Fleet");
			return new Dimension(
				fleetRectSize.width + 2 + textSize.width,
				(int)Math.max(fleetRectSize.height, textSize.height));
		}

		public void render(Graphics g, Point point)
		{
			Dimension fleetRectSize = fleetRectSize(g, numShips);
			drawFleetRect(
				g,
				point.x + fleetRectSize.width / 2,
				point.y - fleetRectSize.height / 2,
				numShips);
			g.drawString("  Fleet", point.x + fleetRectSize.width + 2, point.y);
		}
	}

	class UnownedStarIcon implements LegendItem
	{
		public Dimension size(Graphics g)
		{
			Dimension textSize = textSize(g, "  Unowned Star");
			int height = (int)Math.max(textSize.height, STAR_RADIUS * 2);
			return new Dimension(STAR_RADIUS * 2 + textSize.width, height);
		}

		public void render(Graphics g, Point point)
		{
			g.setColor(UNOWNED_STAR_COLOR);
			drawAsterix(g, point.x + STAR_RADIUS, point.y - STAR_RADIUS);
			g.drawString("  Unowned Star", point.x + STAR_RADIUS * 2 + 2, point.y);
		}
	}

	class RangeDisplay implements LegendItem
	{
		public Dimension size(Graphics g)
		{
			return textSize(g, getText(1000));
		}

		public void render(Graphics g, Point point)
		{
			if (moveSource == null || mousePoint == null)
				return;

			g.setColor(Color.blue);
			int originX = getStarPixelX(moveSource);
			int originY = getStarPixelY(moveSource);
			g.drawLine(originX, originY, mousePoint.x, mousePoint.y);

			int targetX = mousePoint.x;
			int targetY = mousePoint.y;

			double distance;
			if (moveTarget != null && moveTarget != moveSource)
			{
				int dx = moveTarget.x - moveSource.x;
				int dy = moveTarget.y - moveSource.y;
				distance = Math.sqrt(dx * dx + dy * dy);
			}
			else
			{
				int dx = targetX - originX;
				int dy = targetY - originY;
				distance = pixelsToParsecs(Math.sqrt(dx * dx + dy * dy));
			}

			String rangeText = getText(distance);
			g.setColor(Color.white);
			g.drawString(rangeText, point.x, point.y);
		}

		private String getText(double distance)
		{
			DecimalFormat format = new DecimalFormat("###.00");
			return "Distance : " + format.format(distance);
		}
	}

	class Star
	{
		public int x;
		public int y;
		public String name;
		public String owner;
		public boolean isDead;
		public int wealth = -1;
		public int numShips = -1;
		public int numFactories = -1;
		public boolean hasDeathShield = false;
		public boolean hasSpyShield = false;

		Star(ParameterTokenizer tok)
		{
			x = Integer.parseInt(tok.nextToken());
			y = Integer.parseInt(tok.nextToken());
			name = tok.nextToken();
			owner = tok.nextToken();
			isDead = Integer.parseInt(tok.nextToken()) == 1;

			String wealthStr = tok.nextToken();
			if (wealthStr != null)
				wealth = Integer.parseInt(wealthStr);

			String numShipsStr = tok.nextToken();
			if (numShipsStr != null)
				numShips = Integer.parseInt(numShipsStr);

			String numFactoriesStr = tok.nextToken();
			if (numFactoriesStr != null)
				numFactories = Integer.parseInt(numFactoriesStr);

			String hasDeathShieldStr = tok.nextToken();
			if (hasDeathShieldStr != null)
				hasDeathShield = Integer.parseInt(hasDeathShieldStr) == 1;

			String hasSpyShieldStr = tok.nextToken();
			if (hasSpyShieldStr != null)
				hasSpyShield = Integer.parseInt(hasSpyShieldStr) == 1;
		}

		public String toString()
		{
			return name + "( " + x + ", " + y + " )";
		}

		public void render(Graphics g)
		{
			int x = getStarPixelX(this);
			int y = getStarPixelY(this);

			// System.out.println("Rendering to " + x + ", " + y);

			g.setFont(DEFAULT_FONT);

			if (isDead)
			{ // Draw the star in gray if its been death probed.
				g.setColor(DARK_GRAY);
			}
			else
			{ // Set the color to the Stars owner
				g.setColor(getPlayerColor(owner));
			}

			if (this != moveSource && this != moveTarget)
			{
				drawAsterix(g, x, y);
			}
			else
			{
				// Draw it as a circle
				g.fillOval(
					x - STAR_RADIUS,
					y - STAR_RADIUS,
					STAR_RADIUS * 2 + 1,
					STAR_RADIUS * 2 + 1);
			}

			boolean viewerIsOwner = !isDead && player.equals(owner);
			if (viewerIsOwner)
			{
				if (showInfo)
				{
					g.setFont(DEFAULT_FONT);
					// Draw wealth and ships
					g.drawString(
						wealth + ":" + numShips,
						x + 2 * STAR_RADIUS,
						y + 2 * STAR_RADIUS);
					// Draw factories
					StringBuffer buf = new StringBuffer();
					if (numFactories > 0)
						buf.append(Integer.toString(numFactories));
					if (hasSpyShield)
					{
						if (buf.length() > 0)
							buf.append(":");
						buf.append("PS");
					}
					if (hasDeathShield)
					{
						if (buf.length() > 0)
							buf.append(":");
						buf.append("NS");
					}
					g.drawString(
						buf.toString(),
						x - STAR_RADIUS,
						y + 2 * STAR_RADIUS + DEFAULT_FONT.getSize() - 2);
				}
			}
			if (showNames)
			{
				if (viewerIsOwner && (numFactories > 0))
				{ // Bold the names with factories
					g.setFont(BOLD_FONT);
				}
				// Draw the star's name above the star
				FontMetrics metrics = g.getFontMetrics();
				int width = metrics.stringWidth(name);
				g.drawString(name, x - width / 2, y - STAR_RADIUS - 3);
			}
			if ( this == moveSource )
			{
				// Draw white circle at location
				int radius = parsecsToPixels(range);
				g.setColor(WHITE);
				g.drawOval(x - radius, y - radius, radius * 2, radius * 2);
			}
			if ( this == zoomStar && getSelectionAnimationRadius() > 0 )
			{
				int radius = getSelectionAnimationRadius();
				g.setColor(Color.yellow);
				g.drawOval( x - radius, y - radius, 2 * radius, 2 * radius );
			}
		}
	}

	class Fleet
	{
		public Star origin;
		public Star destination;
		public int numShips;
		public int percentTraveled;
		public String unitType;

		Fleet(ParameterTokenizer tok)
		{
			String originStr = tok.nextToken();
			String destinationStr = tok.nextToken();
			origin = getStar(originStr);
			destination = getStar(destinationStr);
			numShips = Integer.parseInt(tok.nextToken());
			percentTraveled =
				(int) (Double.valueOf(tok.nextToken()).doubleValue());
			unitType = tok.nextToken();
		}

		public double getX()
		{
			int origX = origin.x;
			int destX = destination.x;
			return origX + (destX - origX) * percentTraveled / 100.0f;
		}

		public double getY()
		{
			int origY = origin.y;
			int destY = destination.y;
			return origY + (destY - origY) * percentTraveled / 100.0f;
		}

		public void render(Graphics g)
		{
			g.setColor(WHITE);

			int origX = getStarPixelX(origin);
			int origY = getStarPixelY(origin);
			int destX = getStarPixelX(destination);
			int destY = getStarPixelY(destination);

			int x = getPixelX(getX());
			int y = getPixelY(getY());

			// Draw line from start to end
			drawLine(g, origX, origY, destX, destY, x, y);

			g.setFont(DEFAULT_FONT);

			if ("Ship".equals(unitType))
			{
				drawFleetRect(g, x, y, numShips);
			}
			else
			{
				Color color;
				if ("SpyProbe".equals(unitType))
					color = PROBE_COLOR;
				else
					color = BOMB_COLOR;

				drawFleetOval(g, getPixelX(getX()), getPixelY(getY()), color);
			}
		}

		/*
		 * Draws the first half of the path as dashes about 5 pixels long, the second half as
		 * a solid line
		 */
		private void drawLine(
			Graphics g,
			int origX,
			int origY,
			int destX,
			int destY,
			int currentX,
			int currentY)
		{
			g.setColor(VERY_LIGHT_GRAY);
			g.drawLine(origX, origY, currentX, currentY);

			g.setColor(WHITE);
			drawDashedLine(g, currentX, currentY, destX, destY);
		}

		private void drawDashedLine(
			Graphics g,
			int origX,
			int origY,
			int destX,
			int destY)
		{
			int dx = destX - origX;
			int dy = destY - origY;
			double length = Math.sqrt(dx * dx + dy * dy);
			double position = 0;
			while (position < length)
			{
				int startX = (int) (origX + dx * (position / length));
				int startY = (int) (origY + dy * (position / length));

				double endPosition = position + DASH_LENGTH;
				endPosition =
					(endPosition <= length ? endPosition : endPosition);
				int endX = (int) (origX + dx * (endPosition / length));
				int endY = (int) (origY + dy * (endPosition / length));
				g.drawLine(startX, startY, endX, endY);

				// Advance by the length of a dash and a space
				position += DASH_LENGTH * 2;
			}
		}
	}

	static class ParameterTokenizer
	{
		private final String value;

		private int index;

		public ParameterTokenizer(String value)
		{
			if (value == null || "".equals(value))
				throw new IllegalArgumentException("Missing parameter");
			this.value = value;
			this.index = 0;
		}

		public boolean hasNextToken()
		{
			return index < value.length();
		}

		public String nextToken()
		{
			if (!hasNextToken())
				return null;

			StringBuffer sb = new StringBuffer();
			boolean escape = false, done = false;
			for (; !done && index < value.length(); ++index)
			{
				char c = value.charAt(index);
				if (escape)
				{
					sb.append(c);
					escape = false;
				}
				else
				{
					if (c == ESCAPE_CHAR)
						escape = true;
					else if (c != SEPARATOR_CHAR)
						sb.append(c);
					else
						done = true;
				}
			}
			if (sb.length() == 0)
				return null;
			else
				return sb.toString().trim();
		}
	}
}
