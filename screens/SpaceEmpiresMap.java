// Decompiled by JAD v1.5.5. Copyright 1997-98 Pavel Kouznetsov.
// JAD Home Page:      http://web.unicom.com.cy/~kpd/jad.html
// Decompiler options: packimports(3) 
// Source File Name:   SpaceEmpiresMap128.java

import java.applet.Applet;
import java.awt.*;

public class SpaceEmpiresMap128 extends Applet
{
    /* member class not found */
    class Star {}

    /* member class not found */
    class Order {}


    public void init()
    {
        showFleets = false;
        showRange = false;
        showInfo = true;
        showGrid = true;
        showNames = true;
        gridSize = 20;
        showHelp = false;
        showOrders = true;
        String s2 = getParameter("showfleets");
        String s3 = getParameter("showrange");
        String s4 = getParameter("showinfo");
        String s5 = getParameter("showgrid");
        String s6 = getParameter("shownames");
        if(s2.equals("yes"))
            showFleets = true;
        if(s3.equals("yes"))
            showRange = true;
        if(s4.equals("no"))
            showInfo = false;
        if(s5.equals("no"))
            showGrid = false;
        if(s6.equals("no"))
            showNames = false;
        Integer integer = Integer.valueOf(getParameter("gridsize"));
        gridSize = integer.intValue();
        allocateColors();
        setBackground(Color.black);
        numberOfStars = Integer.valueOf(getParameter("stars"));
        numberOfFleets = Integer.valueOf(getParameter("fleets"));
        player = getParameter("player");
        maxRange = Double.valueOf(getParameter("maxrange"));
        strCenter = getParameter("center");
        String s = strCenter.substring(0, 3);
        String s1 = strCenter.substring(3, 6);
        Integer integer1 = Integer.valueOf(s);
        Integer integer2 = Integer.valueOf(s1);
        centerX = integer1.intValue();
        centerY = integer2.intValue();
        String s7 = getParameter("playercolor");
        String s8 = s7.substring(0, 3);
        String s9 = s7.substring(3, 6);
        String s10 = s7.substring(6, 9);
        Integer integer3 = Integer.valueOf(s8);
        Integer integer4 = Integer.valueOf(s9);
        Integer integer5 = Integer.valueOf(s10);
        int i = integer3.intValue();
        int j = integer4.intValue();
        int k = integer5.intValue();
        thisPlayerColor = new Color(i, j, k);
        for(int l = 0; l < numberOfStars.intValue(); l++)
        {
            String s11 = "star" + (l + 1);
            star[l] = getParameter(s11);
        }

        for(int i1 = 0; i1 < numberOfFleets.intValue(); i1++)
        {
            String s12 = "fleet" + (i1 + 1);
            fleet[i1] = getParameter(s12);
        }

    }

    public void allocateColors()
    {
        new Color(255, 255, 255);
        new Color(0, 0, 0);
        new Color(255, 51, 51);
        new Color(51, 255, 51);
        new Color(0, 0, 204);
        new Color(102, 102, 255);
        Color color = new Color(204, 204, 204);
        new Color(0, 204, 255);
        new Color(255, 255, 0);
        new Color(51, 51, 51);
        new Color(255, 102, 51);
        new Color(255, 153, 255);
        new Color(0, 255, 153);
        new Color(236, 224, 155);
        new Color(255, 179, 217);
        Color color1 = new Color(255, 255, 51);
        Color color2 = new Color(255, 153, 255);
        Color color3 = new Color(255, 153, 0);
        Color color4 = new Color(0, 255, 153);
        Color color5 = new Color(236, 224, 155);
        Color color6 = new Color(255, 136, 136);
        Color color7 = new Color(255, 51, 51);
        Color color8 = new Color(0, 255, 255);
        Color color9 = new Color(255, 69, 193);
        Color color10 = new Color(255, 102, 51);
        Color color11 = new Color(153, 109, 255);
        Color color12 = new Color(0, 153, 255);
        playerColor[0] = color;
        playerColor[1] = color1;
        playerColor[2] = color2;
        playerColor[3] = color3;
        playerColor[4] = color4;
        playerColor[5] = color5;
        playerColor[6] = color6;
        playerColor[7] = color7;
        playerColor[8] = color8;
        playerColor[9] = color9;
        playerColor[10] = color10;
        playerColor[11] = color11;
        playerColor[12] = color12;
    }

    public boolean mouseDown(Event event, int i, int j)
    {
        dragX = i;
        dragY = j;
        centerX -= size().width / gridSize / 2 - i / gridSize;
        centerY -= size().height / gridSize / 2 - j / gridSize;
        if(centerX < 5)
            centerX = 5;
        if(centerX > 45)
            centerX = 45;
        if(centerY < 5)
            centerY = 5;
        if(centerY > 45)
            centerY = 45;
        repaint();
        return true;
    }

    public boolean mouseDrag(Event event, int i, int j)
    {
        boolean flag = false;
        int k = (i - dragX) / gridSize;
        int l = (j - dragY) / gridSize;
        if(k >= 1)
        {
            k = 1;
            dragX = i;
            flag = true;
        }
        else
        if(k <= -1)
        {
            k = -1;
            dragX = i;
            flag = true;
        }
        if(l >= 1)
        {
            l = 1;
            dragY = j;
            flag = true;
        }
        else
        if(l <= -1)
        {
            l = -1;
            dragY = j;
            flag = true;
        }
        centerX -= k;
        centerY -= l;
        if(centerX < 5)
            centerX = 5;
        if(centerX > 45)
            centerX = 45;
        if(centerY < 5)
            centerY = 5;
        if(centerY > 45)
            centerY = 45;
        if(flag)
            repaint();
        return true;
    }

    public boolean keyDown(Event event, int i)
    {
        switch(i)
        {
        case 1005: 
            centerY++;
            break;

        case 1004: 
            centerY--;
            break;

        case 1007: 
            centerX++;
            break;

        case 1006: 
            centerX--;
            break;

        case 45: /* '-' */
            gridSize -= 2;
            break;

        case 43: /* '+' */
            gridSize += 2;
            break;

        case 61: /* '=' */
            gridSize += 2;
            break;

        case 70: /* 'F' */
            showFleets = !showFleets;
            break;

        case 102: /* 'f' */
            showFleets = !showFleets;
            break;

        case 71: /* 'G' */
            showGrid = !showGrid;
            break;

        case 103: /* 'g' */
            showGrid = !showGrid;
            break;

        case 72: /* 'H' */
            showHelp = true;
            break;

        case 104: /* 'h' */
            showHelp = true;
            break;

        case 63: /* '?' */
            showHelp = true;
            break;

        case 1008: 
            showHelp = true;
            break;

        case 73: /* 'I' */
            showInfo = !showInfo;
            break;

        case 105: /* 'i' */
            showInfo = !showInfo;
            break;

        case 78: /* 'N' */
            showNames = !showNames;
            break;

        case 110: /* 'n' */
            showNames = !showNames;
            break;

        case 79: /* 'O' */
            showOrders = !showOrders;
            break;

        case 111: /* 'o' */
            showOrders = !showOrders;
            break;

        case 82: /* 'R' */
            showRange = !showRange;
            break;

        case 114: /* 'r' */
            showRange = !showRange;
            break;

        default:
            currkey = i;
            break;

        }
        if(centerX < 5)
            centerX = 5;
        if(centerX > 45)
            centerX = 45;
        if(centerY < 5)
            centerY = 5;
        if(centerY > 45)
            centerY = 45;
        if(gridSize < 6)
            gridSize = 6;
        if(gridSize > 50)
            gridSize = 50;
        repaint();
        return true;
    }

    public void drawGrid(Graphics g)
    {
        Color color = new Color(51, 51, 51);
        g.setColor(color);
        for(x1 = 0; x1 < size().width; x1 = x1 + gridSize)
        {
            g.drawLine(x1, 0, x1, size().height);
            g.drawLine(0, x1, size().width, x1);
        }

    }

    public void showHelp(Graphics g)
    {
        Color color = new Color(0, 0, 204);
        g.setColor(color);
        g.fillRect(25, 25, 300, 320);
        g.setColor(Color.white);
        g.drawRect(25, 25, 300, 320);
        g.setFont(f14b);
        g.drawString("HegemonyMap version 1.28", 35, 40);
        g.setFont(f9);
        g.drawString("October 6, 2002", 35, 55);
        g.setFont(f12);
        g.drawString("Toggle Keys:", 35, 80);
        g.drawString("F = view Fleets", 50, 100);
        g.drawString("I = view Production/Ship Info", 50, 120);
        g.drawString("O = view Standing Orders", 50, 140);
        g.drawString("R = view Range Circles", 50, 160);
        g.drawString("G = view Gridlines", 50, 180);
        g.drawString("N = view Star Names", 50, 200);
        g.drawString("Other Keys:", 35, 240);
        g.drawString("+ = zoom in", 50, 260);
        g.drawString("- = zoom out", 50, 280);
        g.drawString("arrows/drag = scroll", 50, 300);
        g.setFont(f9);
        g.drawString("Press any key to close this info box.", 35, 330);
        showHelp = false;
    }

    public void showFleets(Graphics g)
    {
        Color color = new Color(0, 0, 204);
        Color color1 = new Color(204, 0, 0);
        Color color2 = new Color(0, 102, 0);
        g.setColor(Color.white);
        g.setFont(f9);
        for(int i2 = 0; i2 < numberOfFleets.intValue(); i2++)
        {
            Integer integer = Integer.valueOf(fleet[i2].substring(0, 3));
            Integer integer1 = Integer.valueOf(fleet[i2].substring(3, 6));
            Integer integer2 = Integer.valueOf(fleet[i2].substring(7, 10));
            Integer integer3 = Integer.valueOf(fleet[i2].substring(10, 13));
            Integer integer4 = Integer.valueOf(fleet[i2].substring(14, 19));
            Integer integer5 = Integer.valueOf(fleet[i2].substring(20, 22));
            String s = fleet[i2].substring(23, 24);
            int i = integer.intValue();
            int j = integer1.intValue();
            int k = integer2.intValue();
            int l = integer3.intValue();
            int i1 = integer4.intValue();
            int j1 = integer5.intValue();
            i = ((size().width / gridSize / 2 - centerX) + i) * gridSize;
            j = ((size().height / gridSize / 2 - centerY) + j) * gridSize;
            k = ((size().width / gridSize / 2 - centerX) + k) * gridSize;
            l = ((size().height / gridSize / 2 - centerY) + l) * gridSize;
            g.drawLine(i, j, k, l);
            g.drawOval(k - 5, l - 5, 10, 10);
            int k1 = i + (j1 * (k - i)) / 100;
            int l1 = j + (j1 * (l - j)) / 100;
            g.setColor(color);
            if(s.equals("D"))
            {
                g.setColor(color1);
                g.fillRect(k1 - 4, l1 - 5, 8, 10);
                g.setColor(Color.white);
                g.drawRect(k1 - 4, l1 - 5, 8, 10);
                g.drawString("D", k1 - 3, l1 + 4);
            }
            else
            if(s.equals("S"))
            {
                g.setColor(color2);
                g.fillRect(k1 - 4, l1 - 5, 8, 10);
                g.setColor(Color.white);
                g.drawRect(k1 - 4, l1 - 5, 8, 10);
                g.drawString("S", k1 - 2, l1 + 4);
            }
            else
            if(s.equals("A"))
            {
                g.setColor(color1);
                int ai[] = {
                    k1 - 5, k1, k1 + 5, k1
                };
                int ai1[] = {
                    l1, l1 - 5, l1, l1 + 5
                };
                g.fillPolygon(ai, ai1, ai.length);
                g.setColor(Color.white);
                g.drawPolygon(ai, ai1, ai.length);
            }
            else
            if(i1 < 10)
            {
                g.fillRect(k1 - 4, l1 - 5, 8, 10);
                g.setColor(Color.white);
                g.drawRect(k1 - 4, l1 - 5, 8, 10);
                g.drawString(String.valueOf(i1), k1 - 2, l1 + 4);
            }
            else
            if(i1 < 100)
            {
                g.fillRect(k1 - 6, l1 - 5, 13, 10);
                g.setColor(Color.white);
                g.drawRect(k1 - 6, l1 - 5, 13, 10);
                g.drawString(String.valueOf(i1), k1 - 4, l1 + 4);
            }
            else
            if(i1 < 1000)
            {
                g.fillRect(k1 - 9, l1 - 5, 18, 10);
                g.setColor(Color.white);
                g.drawRect(k1 - 9, l1 - 5, 18, 10);
                g.drawString(String.valueOf(i1), k1 - 7, l1 + 4);
            }
            else
            {
                g.fillRect(k1 - 11, l1 - 5, 23, 10);
                g.setColor(Color.white);
                g.drawRect(k1 - 11, l1 - 5, 23, 10);
                g.drawString(String.valueOf(i1), k1 - 9, l1 + 4);
            }
        }

    }

    public void drawStars(Graphics g)
    {
        boolean flag = false;
        boolean flag1 = false;
        boolean flag2 = false;
        boolean flag4 = false;
        String as[] = new String[10];
        Color color = new Color(51, 51, 51);
        Color color1 = new Color(51, 51, 51);
        Color color2 = new Color(100, 100, 100);
        int k1 = (int)(maxRange.doubleValue() * gridSize);
        int j2 = 0;
        for(int i = 0; i < numberOfStars.intValue(); i++)
        {
            int j1;
            boolean flag3 = false; j1 = 0;
            for(int l = 0; l < as.length; l++)
            {
                int i1 = star[i].indexOf("|", j1);
                if(i1 > -1)
                    as[l] = star[i].substring(j1, i1);
                else
                    as[l] = star[i].substring(j1);
                j1 = i1 + 1;
            }

            String s = as[0].substring(0, 3);
            String s1 = as[0].substring(3, 6);
            StarData[i] = new Star();
            StarData[i].x = Integer.valueOf(s).intValue();
            StarData[i].y = Integer.valueOf(s1).intValue();
            StarData[i].name = as[1];
            StarData[i].name = StarData[i].name.trim();
            StarData[i].strOwner = as[2];
            StarData[i].strOwner = StarData[i].strOwner.trim();
            StarData[i].intOwner = Integer.valueOf(StarData[i].strOwner).intValue();
            StarData[i].wealth = as[3];
            StarData[i].ships = as[4];
            StarData[i].factories = as[5];
            StarData[i].deathShield = as[6];
            StarData[i].spyShield = as[7];
            StarData[i].systemSpecial = as[8];
            StarData[i].wayPoint = as[9];
            if(!StarData[i].wayPoint.equals("") && !StarData[i].wealth.equals("???"))
            {
                OrderData[j2] = new Order();
                OrderData[j2].sourceX = StarData[i].x;
                OrderData[j2].sourceY = StarData[i].y;
                OrderData[j2].destX = 0;
                OrderData[j2].destY = 0;
                int k2 = StarData[i].wayPoint.indexOf("-");
                if(k2 > 0)
                    OrderData[j2].waypointName = StarData[i].wayPoint.substring(0, k2);
                else
                    OrderData[j2].waypointName = "";
                j2++;
            }
        }

        if(showOrders)
        {
            for(int j = 0; j < j2; j++)
            {
                for(int l2 = 0; l2 < numberOfStars.intValue(); l2++)
                    if(OrderData[j].waypointName.compareTo(StarData[l2].name) == 0)
                    {
                        OrderData[j].destX = StarData[l2].x;
                        OrderData[j].destY = StarData[l2].y;
                    }

                int i3 = (size().width / gridSize / 2 - centerX) + OrderData[j].sourceX;
                int j3 = (size().height / gridSize / 2 - centerY) + OrderData[j].sourceY;
                int k3 = (size().width / gridSize / 2 - centerX) + OrderData[j].destX;
                int l3 = (size().height / gridSize / 2 - centerY) + OrderData[j].destY;
                g.setColor(color2);
                g.drawLine(i3 * gridSize, j3 * gridSize, k3 * gridSize, l3 * gridSize);
                g.drawOval(k3 * gridSize - 3, l3 * gridSize - 3, 6, 6);
            }

        }
        for(int k = 0; k < numberOfStars.intValue(); k++)
        {
            int l1 = (size().width / gridSize / 2 - centerX) + StarData[k].x;
            int i2 = (size().height / gridSize / 2 - centerY) + StarData[k].y;
            if(StarData[k].intOwner == 99)
                g.setColor(color1);
            else
                g.setColor(playerColor[StarData[k].intOwner]);
            g.setFont(f9);
            if(!StarData[k].wealth.equals("???"))
            {
                g.setColor(thisPlayerColor);
                if(showRange)
                {
                    g.setColor(color);
                    g.drawOval(l1 * gridSize - k1, i2 * gridSize - k1, k1 * 2, k1 * 2);
                    g.setColor(playerColor[StarData[k].intOwner]);
                    if(!StarData[k].wealth.equals("???"))
                        g.setColor(thisPlayerColor);
                }
                if(showInfo)
                {
                    String s2 = "";
                    if(StarData[k].deathShield.equals("Y"))
                        s2 = "DS";
                    if(StarData[k].spyShield.equals("Y"))
                        if(!s2.equals(""))
                            s2 = s2 + ":SS";
                        else
                            s2 = "SS";
                    g.drawString(StarData[k].wealth.trim() + ":" + StarData[k].ships.trim(), l1 * gridSize + 6, i2 * gridSize + 6);
                    if(!StarData[k].factories.equals("   0") && !s2.equals(""))
                        g.drawString(StarData[k].factories.trim() + ":" + s2, l1 * gridSize - 3, i2 * gridSize + 15);
                    else
                    if(!s2.equals(""))
                        g.drawString(s2, l1 * gridSize - 3, i2 * gridSize + 15);
                    else
                    if(!StarData[k].factories.equals("   0"))
                        g.drawString(StarData[k].factories.trim(), l1 * gridSize - 3, i2 * gridSize + 15);
                }
            }
            if(showNames)
            {
                g.setFont(f11b);
                if(StarData[k].factories.equals("   0") || StarData[k].factories.equals("????"))
                    g.setFont(f11);
                g.drawString(StarData[k].name, l1 * gridSize - 3, i2 * gridSize - 5);
            }
            if(StarData[k].systemSpecial.equals("NO") || StarData[k].systemSpecial.equals("??") || StarData[k].systemSpecial.equals(" "))
            {
                g.drawLine(l1 * gridSize + 3, i2 * gridSize, l1 * gridSize - 3, i2 * gridSize);
                g.drawLine(l1 * gridSize, i2 * gridSize + 3, l1 * gridSize, i2 * gridSize - 3);
                g.drawLine(l1 * gridSize + 3, i2 * gridSize + 3, l1 * gridSize - 3, i2 * gridSize - 3);
                g.drawLine(l1 * gridSize - 3, i2 * gridSize + 3, l1 * gridSize + 3, i2 * gridSize - 3);
            }
            else
            if(StarData[k].systemSpecial.equals("SS"))
            {
                g.fillOval(l1 * gridSize - 4, i2 * gridSize - 4, 9, 9);
                g.setColor(Color.black);
                g.fillOval(l1 * gridSize + 1, i2 * gridSize - 3, 2, 2);
                g.drawLine(l1 * gridSize - 4, i2 * gridSize, l1 * gridSize + 4, i2 * gridSize);
            }
        }

    }

    public void paint(Graphics g)
    {
        if(showGrid)
            drawGrid(g);
        drawStars(g);
        if(showFleets)
            showFleets(g);
        if(showHelp)
            showHelp(g);
    }

    public SpaceEmpiresMap128()
    {
        playerColor = new Color[20];
        thisPlayerColor = new Color(0, 204, 51);
        centerX = 10;
        centerY = 10;
        star = new String[200];
        StarData = new Star[200];
        OrderData = new Order[200];
        fleet = new String[200];
        f14b = new Font("Helvetica", 1, 14);
        f12 = new Font("Helvetica", 0, 12);
        f12b = new Font("Helvetica", 1, 12);
        f11 = new Font("Helvetica", 0, 11);
        f11b = new Font("Helvetica", 1, 11);
        f10 = new Font("Helvetica", 0, 10);
        f9 = new Font("Helvetica", 0, 9);
        f8 = new Font("Helvetica", 0, 8);
    }

    Integer numberOfStars;
    Integer numberOfFleets;
    Double maxRange;
    String strCenter;
    String player;
    boolean showInfo;
    boolean showNames;
    boolean showGrid;
    boolean showFleets;
    boolean showRange;
    boolean showHelp;
    boolean showOrders;
    int gridSize;
    int currkey;
    int x1;
    int x2;
    int y1;
    int y2;
    int newX;
    int newY;
    Color playerColor[];
    Color thisPlayerColor;
    int centerX;
    int centerY;
    int dragX;
    int dragY;
    String star[];
    Star StarData[];
    Order OrderData[];
    String fleet[];
    Font f14b;
    Font f12;
    Font f12b;
    Font f11;
    Font f11b;
    Font f10;
    Font f9;
    Font f8;
}
