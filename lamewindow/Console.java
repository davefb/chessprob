import javax.swing.*;
import java.util.*;

// A simple Java Console for your application (Swing version)
// Requires Java 1.1.5 or higher
//
// Disclaimer the use of this source is at your own risk. 
//
// Permision to use and distribute into your own applications
//
// RJHM van den Bergh , rvdb@comweb.nl
 
import java.io.*;
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
 
public class Console extends WindowAdapter implements WindowListener, ActionListener, Runnable
{
	private JFrame frame;
	private JTextArea textArea;
	private Thread reader;
	private Thread reader2;
	private boolean quit;
					
	private final InputStream pin=(System.in); 
 
	Thread errorThrower; // just for testing (Throws an Exception at this Console
	
	public Console()
	{
		// create all components and add them
	    frame=new JFrame("Chess Console");
		Dimension screenSize=Toolkit.getDefaultToolkit().getScreenSize();
		Dimension frameSize=new Dimension((int)(screenSize.width/4),(int)(screenSize.height/4));
		int x=(int)(frameSize.width/4);
		int y=(int)(frameSize.height/4);
		frame.setBounds(x,y,frameSize.width,frameSize.height);
		
		textArea=new JTextArea();
		textArea.setLineWrap(true);
		textArea.setWrapStyleWord(true);

		textArea.setEditable(false);
		JButton button=new JButton("clear");
		
		frame.getContentPane().setLayout(new BorderLayout());
		frame.getContentPane().add(new JScrollPane(textArea),BorderLayout.CENTER);
		frame.getContentPane().add(button,BorderLayout.SOUTH);
		frame.setVisible(true);		
		
		frame.addWindowListener(this);		
		button.addActionListener(this);
		
		reader = new Thread(this);
		reader.setDaemon(true);
		reader.start();
	}
	
	public synchronized void windowClosed(WindowEvent evt)
	{
		quit=true;
		this.notifyAll(); // stop all threads
		try { reader.join(1000);pin.close();   } catch (Exception e){}		
		System.exit(0);
	}		
		
	public synchronized void windowClosing(WindowEvent evt)
	{
		frame.setVisible(false); // default behaviour of JFrame	
		frame.dispose();
	}
	
	public synchronized void actionPerformed(ActionEvent evt)
	{
		textArea.setText("");
	}
    
	public synchronized void run()
	{
		try
		{			
		    while(true){
			this.wait(100);
			String s =this.readLine(this.pin);
			if(s.indexOf('\t')!=-1){
			    s = s.substring(s.indexOf('\t')+1);
			    textArea.setText("");
			}
			textArea.append(s);
			if (quit) return;
		    }
		} 
		catch (Exception e)
		{
			textArea.append("\nConsole reports an Internal error.");
			textArea.append("The error is: "+e);			
		}
	}
	
	public synchronized String readLine(InputStream in) throws IOException
	{
		String input="";
		do
		{
			int available=in.available();
			if (available==0) break;
			byte b[]=new byte[available];
			in.read(b);
			input=input+new String(b,0,b.length);				
			System.out.println("reading\n");
		}while( !input.endsWith("\n") &&  !input.endsWith("\r\n") && !quit);
		return input;
	}	
		
	public static void main(String[] arg)
	{
		new Console(); // create console with not reference	
	}			
}
