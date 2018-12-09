package acdc;
import java.util.*;

import javax.swing.JFrame;
import javax.swing.JScrollPane;
import javax.swing.JTree;
import javax.swing.tree.DefaultMutableTreeNode;

/**
 * This application facilitates the task of recovering the structure
 * of large and complex software systems in an automatic way by clustering.
 * 
 * The data structure used to represent the components of the software system
 * is a tree, which is clustered incrementally by using several patterns. 
 * 
 * Assumptions made:
 * ACDC will cluster the children of the root in the input.
 * Once an object has been clustered, it is never removed from its cluster
 * (but it might get further clustered within its cluster)
 */
public class ACDC
{

/**
 * Exits the program with an error message which reminds the user how to
 * run this application. 
 * The string s represents the concatenation of characters representing
 * allowable clustering patterns to be used in this program, e.g. 'b' - 
 * body-header pattern, 's'- subgraph pattern , 'o' - orphan adoption etc.
 * @param run_name 
 */
  static void err_AND_exit(String run_name)
  {
	IO.put("USAGE: " + run_name  + " <.ta or .rsf input file> <.rsf output file> [-/+patterns] [options]",0);
		
		IO.put("\nSupported patterns include:",0);
  		IO.put("  B              Body Header",0);
  		IO.put("  S              SubGraph Dominator",0);
  		IO.put("  O              Orphan Adoption",0);
		IO.put("Pattern formats:",0);
		IO.put("<no pattern>     Assumes an input of +BSO and executes the patterns in that order",0);
		IO.put("+pattern(s)      Executes ONLY specified patterns in the given order",0);
		IO.put("-pattern(s)	     Assumes an execution of patterns given by +BSO but removes specified",0); 
		IO.put("                 patterns and executes remaining ones",0);
		
		IO.put("\nPossible options include:",0);
		IO.put("  -d1            Prints progress report messages to standard output",0);
		IO.put("  -d2            Prints detailed debugging info to standard output",0);
 		IO.put("  -h             Prints this synopsis of standard options and exits (other arguments are ignored)",0);
		IO.put("  -l[integer]    Requests that clusters formed in SubGraph have a maximum size\n",0); 		      
  		IO.put("By default, ACDC generates a flat decomposition containing fine-grained clusters.",0);
  		IO.put("The following options can modify this:",0);
		IO.put("  -a[systemName] Generates a hierarchical decomposition (contains nested clusters)",0);
		IO.put("  -u	     Generates a flat decomposition containing only the top level clusters\n",0);
		IO.put("  -t	     Displays the generated decomposition graphically (output file is also created)",0);
		
		System.exit(1);
  }

/**
 * Returns true if the string s1 is made up only of characters found
 * in the string s2; else returns false.
 */
  private static boolean matches(String s1, String s2)
 {
	boolean containsNoOther = true; 
	Vector v = new Vector(s2.length()); 

	for(int i=0 ; i<s2.length() ; i++)
	    v.add(Character.toString(s2.charAt(i)));
	  
	for(int j=0; j<s1.length(); j++)
	{
		if (v.contains(Character.toString(s1.charAt(j))))
			;
		else 
			containsNoOther = false;    
	}
	return containsNoOther;
  }
  
	private static String subtract (String s1, String s2)
	{
		StringBuffer result = new StringBuffer(s1);
		for (int i=0; i< s2.length(); i++)
		{
			int pos = result.indexOf(s2.substring(i,i+1));
			result = result.replace(pos,pos+1,"");
		}
		return result.toString();
	}
  
  public static void main (String [] args)
  {
    String run_name = "java acdc.ACDC";
    for (int i= 0; i<args.length; i++)
    {
        if (args[i].equals("-6431")) run_name = "acdc";
    }
    
    //if one of the given args is "-h", print Help message, then exit
    for(int u=0; u<args.length; u++)
    {
    	if(args[u].equalsIgnoreCase("-h"))
    	{
			err_AND_exit(run_name);	
    	}
    }
    
	IO.set_debug_level(0);
    
    String inputName, outputName;
    
    int maxClusterSize = 20; //used by SubGraph pattern
    boolean gui = false;
       
    // parse input arguments
    if (args.length<2)
    {   
    	 IO.put("\nToo few arguments.",0);
    	 err_AND_exit(run_name);
    }
    
	inputName = args[0]; 
    outputName = args[1];
 
	InputHandler input = null;
	if(inputName.endsWith(".ta") || inputName.endsWith(".rsf"))
		input = new TAInput();
   
	else if(inputName.endsWith(".gxl"))
	{
		IO.put("GXL input is not supported yet.",0);
		IO.put("Hopefully in the next version...",0);
		System.exit(0);
	}
    
	else
	{
		IO.put("Unrecognized input format",0);
		IO.put("Accepted formats are RSF and TA (extensions .rsf and .ta)",0);
		System.exit(0);
	}
	
	OutputHandler output = null;
    
	if (outputName.endsWith(".rsf"))
	{
		output = new RSFOutput();
	}
	else if (outputName.endsWith(".ta"))
	{
		IO.put("TA is not a supported output format yet.",0);
		IO.put("Hopefully in the next version...",0);
		System.exit(0);
	}
	else if(outputName.endsWith(".gxl"))
	{
		IO.put("GXL is not a supported output format yet.",0);
		IO.put("Hopefully in the next version...",0);
		System.exit(0);
	}
	else
	{
		IO.put("Unrecognized output format",0);
		IO.put("Only RSF is supported at this point (extensions .rsf)",0);
		System.exit(0);
	}
		 
	// If it got to this line, we are dealing with at least two args
	// Code executes for 2 or more arguments 

	final String defaultPatterns = "bso";
	String selectedPatterns = null;
    boolean patternsSpecified = false;
    Pattern inducer = null;
	
	// Create a tree with a dummy root
	Node dummy = new Node ("ROOT", "Dummy");
	DefaultMutableTreeNode root = new DefaultMutableTreeNode (dummy);
	dummy.setTreeNode(root);
	
	for (int i= 2; i<args.length; i++)
	{
		final boolean startsWithPlus = args[i].charAt(0) == '+';
		final boolean startsWithMinus = args[i].charAt(0) == '-';
		final String rest = args[i].substring(1);
		final boolean onlyPatterns = matches(rest, defaultPatterns);
		if (startsWithPlus && onlyPatterns)
		{
			if (patternsSpecified)
			{
				IO.put("Duplicate pattern option.",0);
				System.exit(0);
			}
			else
			{
				selectedPatterns = rest; 
				patternsSpecified = true;
			}
		}
		else if (startsWithMinus && onlyPatterns)
		{
			if (patternsSpecified)
			{
				IO.put("Duplicate pattern option.",0);
				System.exit(0);
			}
			else
			{
				selectedPatterns = subtract(defaultPatterns, rest); 
				patternsSpecified = true;
			}
		}
		else if (startsWithMinus && rest.equalsIgnoreCase("d1"))
		{
			IO.set_debug_level(1);
		}
		else if (startsWithMinus && rest.equalsIgnoreCase("d2"))
		{
			IO.set_debug_level(2);
		}
        else if (startsWithMinus && rest.equalsIgnoreCase("6431"))
        {
            run_name = "acdc";
        }
		else if (startsWithMinus && (rest.charAt(0) == 'l'))
		{
			try
			{ 
				maxClusterSize = Integer.parseInt(rest.substring(1));	
			}
			catch (NumberFormatException n) 
			{
				IO.put("Option -l must be followed by a positive integer.",0);
				System.exit(0);
			}
			if (maxClusterSize < 1)
			{
				IO.put("Option -l must be followed by a positive integer.",0);
				System.exit(0);
			}
		}
		else if (startsWithMinus && rest.equalsIgnoreCase("a"))
		{
			inducer = new FullOutput(root,"ROOT");
		}
		else if (startsWithMinus && (rest.length() > 1) && (rest.substring(0,1).equalsIgnoreCase("a")))
		{
			inducer = new FullOutput(root,rest.substring(1));
		}
		else if (startsWithMinus && rest.equalsIgnoreCase("u"))
		{
			inducer = new UpInducer(root);
		}
		else if (startsWithMinus && rest.equalsIgnoreCase("t"))
		{
			gui = true;
		}
		else
		{
			IO.put("Unrecognized option: " + args[i],0);
			System.exit(0);
		}
	}
	
	if (selectedPatterns == null)
		selectedPatterns = defaultPatterns;
	if (inducer == null)
		inducer = new DownInducer(root);
			   	
    IO.put ("Input File: " + inputName,1);
    IO.put ("Output File: " + outputName,1);
    IO.put("Patterns: " + selectedPatterns,1);
    IO.put("Cluster Size: " + maxClusterSize,1);

	// Populate the tree from the input file   
    input.readInput(inputName, root);
    
//    Pattern b = new BodyHeader(root);
//    Pattern s = new SubGraph(root, maxClusterSize);
//    Pattern o = new OrphanAdoption(root);
//    Pattern r = new ReverseOrphanAdoption(root);
    //Pattern e = new EdgeInduction(root);
    //add new pattern here

	Vector vpatterns = new Vector(); //will contain the ordered patterns to be executed
    
	for(int j=0; j<selectedPatterns.length(); j++)
	{    
		switch (selectedPatterns.charAt(j))
	    {
		case 'b':
		vpatterns.add(new BodyHeader(root));
		//vpatterns.add(b);
			    break;
		case 's':
		vpatterns.add(new SubGraph(root,maxClusterSize)); 
		//vpatterns.add(s); 
			    break;
		case 'o':
		vpatterns.add(new OrphanAdoption(root)); 
		//vpatterns.add(o); 
			    break;
		// Add new pattern here
		default:   
				IO.put("Serious error.",0);
				System.exit (0);
		}
	}

	// Induce all edges
	Vector allNodes = Pattern.allNodes(root);
	Pattern.induceEdges(allNodes, root);

	// Execute the patterns
    Iterator iv = vpatterns.iterator();
    while (iv.hasNext())
    {
		Pattern p = (Pattern) iv.next();
		IO.put("Executing " + p.getName() + " pattern...",1);
		p.execute();
    }

	// Take care of any objects that were not clustered
	Pattern c = new ClusterLast(root);
	c.execute();
	
    // Create output file
	IO.put("Creating output...",1);
	inducer.execute();
	output.writeOutput(outputName, root);
	IO.put("Finished!",1);
    
    // Create GUI 
    if (gui)
    {
		displayTree(root);
    }
  }

	private static void displayTree(DefaultMutableTreeNode root) 
	{
		JTree nodeTree = new JTree (root);
		nodeTree.setShowsRootHandles (true);
		nodeTree.putClientProperty ("JTree.lineStyle", "Horizontal");
		nodeTree.putClientProperty ("JTree.lineStyle", "Angled");
		JFrame frame = new JFrame ("File Node Partition");
		frame.setDefaultCloseOperation (JFrame.EXIT_ON_CLOSE);
		frame.getContentPane ().add (new JScrollPane (nodeTree), "Center");
		frame.setSize (400, 600);
		frame.setVisible (true);
	}
	
}