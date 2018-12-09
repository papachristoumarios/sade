package acdc;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.Enumeration;
import java.util.StringTokenizer;

import javax.swing.tree.DefaultMutableTreeNode;

/**
* This class creates a tree from the info passed 
* by the input file.
*/
public class TAInput implements InputHandler
{
	public void readInput(String inputStr, DefaultMutableTreeNode treeModel)
	{
		String str, firstTok, secondTok, thirdTok;
		IO.put("Reading input...",1);
		try 
		{
			BufferedReader in = new BufferedReader(new FileReader(inputStr));
			str = in.readLine();
			if (str != null)
				str = str.trim();
			else
			{
				// Abort if input file was empty
				IO.put("Empty input file!",1);
				System.exit(0);
			}
	      
			// Skip the lines between "Scheme Tuple" and "Fact Tuple"
			if (str.equals("SCHEME TUPLE :"))
				do
				{
					str = in.readLine();
					str = str.trim();
				} while (!str.equals("FACT TUPLE :"));
	      
			// Skip "Fact Tuple:"
			if (str.equals("FACT TUPLE :")) 
			{
				str = in.readLine();
				str = str.trim();
			}
			
			// Following lines up to end of file or to "Fact Attribute" should contain 3 tokens per line
			do
			{
				StringTokenizer strTok = new StringTokenizer(str);
				
				// If encountering a line which doesn't contain 3 tokens per line, abort with a message
				if(strTok.countTokens() != 3)
				{
					IO.put("Syntax error in input file!",0);
					IO.put("The following tuple contains " + strTok.countTokens() + " tokens:",0);
					IO.put(str,0);
					IO.put("Aborting...",0);
					System.exit(0);
				}

				firstTok  = strTok.nextToken(); //type of relation
				secondTok = strTok.nextToken(); 
				thirdTok  = strTok.nextToken(); 

				/******************************************************************************
				      CASE 1: first token in the line is  "$INSTANCE"
				 ******************************************************************************/
				if (firstTok.equals("$INSTANCE"))
				{ 
					//secondTok <-- name of a node in the tree
					//thirdTok  <-- type of a node in the tree

					// If secondTok has been instantiated before, abort with a message
					DefaultMutableTreeNode root = (DefaultMutableTreeNode)treeModel.getRoot();
					Enumeration allNodes = root.depthFirstEnumeration();
					while (allNodes.hasMoreElements())
					{
						Object i = allNodes.nextElement();
						DefaultMutableTreeNode j = (DefaultMutableTreeNode)i;
						Node n = (Node)j.getUserObject();
						if (n.getName().equals(secondTok))
						{
							IO.put("Syntax error in input file!",0);
							IO.put("Two instances of " + secondTok,0);
							IO.put("Aborting...",0);
							System.exit(0);
						}
					}
					IO.put("TAInput.java:\t$INSTANCE Will create node " + secondTok,2);

					// Create a node and instantiate it with the given name and type
					Node n = new Node(secondTok, thirdTok);
					// Insert the node in the tree under the root
					DefaultMutableTreeNode tn = new DefaultMutableTreeNode(n);
					n.setTreeNode(tn);
					root.add(tn);
				}
				
		/******************************************************************************
		      CASE 2: first token in the line is  "contain"
		*****************************************************************************/
		else if (firstTok.equals("contain"))
		{
		  //secondTok <-- name of a node (maybe) in the tree
		  //thirdTok  <-- name of a node (maybe) in the tree

		  //traverse the tree
		  DefaultMutableTreeNode root = 
					 (DefaultMutableTreeNode)treeModel.getRoot();
		  Enumeration allNodes = root.depthFirstEnumeration();
		  DefaultMutableTreeNode tn1 = null;
		  DefaultMutableTreeNode tn2 = null;
		  
		  //check if the tree already contains a node 
		  //with the same name as secondTok or thirdTok
		  while (allNodes.hasMoreElements())
		  {
		    Object i = allNodes.nextElement();
		    DefaultMutableTreeNode j = (DefaultMutableTreeNode)i;
		    Node n = (Node)j.getUserObject();
		    if (n.getName().equals(secondTok)) tn1 = j;
		    if (n.getName().equals(thirdTok)) tn2 = j;
		  }
		  //if secondTok corresponding node was not found as part of the tree
		  //create a node and add it under root
		  if (tn1 == null) 
		  {
        	    Node n1 = new Node(secondTok, "UnknownContainer");
        	    IO.put("Container of unknown type: " + secondTok + ". Assumed to be a cluster", 2);
		    tn1 = new DefaultMutableTreeNode(n1);
        	    n1.setTreeNode(tn1);
		    root.add(tn1);
		  }
		  //if thirdTok corresponding node was not found as part of the tree
		  //create a node
		  if (tn2 == null) 
        	  {
        	    Node n2 = new Node(thirdTok, "Unknown");
        	    //IO.put("Node of unknown type: "+ thirdTok);
        	    tn2 = new DefaultMutableTreeNode(n2);
        	    n2.setTreeNode(tn2);
        	  }
		  //add thirdTok node under secondTok node
		  tn1.add(tn2);
		  IO.put("TAInput.java:\tcontain " + secondTok + "\t" +thirdTok,2);
		}
		/******************************************************************************
		      CASE 3: first token in the line is other than "$INSTANCE" or "contain"
		*****************************************************************************/
		else
		{
		  //secondTok <-- name of a node in the tree
		  //thirdTok  <-- name of a node in the tree

		  DefaultMutableTreeNode root = 
					 (DefaultMutableTreeNode)treeModel.getRoot();
		  Enumeration allNodes = root.depthFirstEnumeration();
		  
		  DefaultMutableTreeNode tn1 = null;
		  DefaultMutableTreeNode tn2 = null;
		  Node n1 = null;
		  Node n2 = null;
		  
		  //search all tree for nodes with names equal to second or third token
		  while (allNodes.hasMoreElements())
		  {
		    Object i = allNodes.nextElement();
		    DefaultMutableTreeNode j = (DefaultMutableTreeNode)i;
		    Node n = (Node)j.getUserObject();
		    //node with name secondTok was found in the tree
		    if (n.getName().equals(secondTok)) 
		    {
		      tn1 = j;
		      n1 = n;
		    }
		    //node with name thirdTok was found in the tree
		    if (n.getName().equals(thirdTok))
		    {
		      tn2 = j;
		      n2 = n;
		    }
		  }
		  
		  /********************************************************************************************
		   CASES 3.1:  secondTok and thirdTok are same, but do not have a corresponding node in the tree
		   ********************************************************************************************/ 
		  if(secondTok.equals(thirdTok) && tn1==null)
		  {
		    //create only one node and add it under root
		    
		    n1 = new Node(secondTok, "Unknown");
		    //IO.put("Node of unknown type: "+ secondTok);
		    tn1 = new DefaultMutableTreeNode(n1);
		    n1.setTreeNode(tn1);
		    root.add(tn1);//add only one of the two tokens as nodes under the root
		  }
		  
		  /********************************************************************************************
		   CASES 3.2:      secondTok and thirdTok are same and have a corresponding node in the tree
		   ********************************************************************************************/ 
		  else if(secondTok.equals(thirdTok) && tn1!=null)
		  {
			// Do nothing
		  }
		 
		  
		  /********************************************************
		   CASES 3.3:    secondTok and thirdToken are not the same 
		   ********************************************************/ 
		  else 
		  {
		    /******************************************************************************
		      CASE 3.3.1:         secondTok doesn't have a corresponding node in the tree 
		    /*****************************************************************************/
		    if (tn1 == null)
		    {
			//create new node and add it under root
			
			n1 = new Node(secondTok, "Unknown");
			//IO.put("Node of unknown type: "+ secondTok);
			tn1 = new DefaultMutableTreeNode(n1);
			n1.setTreeNode(tn1);
			root.add(tn1);//add it under root
		    }
		    
		    /******************************************************************************
		      CASE 3.3.2:         thirdTok doesn't have a corresponding node in the tree 
		    /*****************************************************************************/
		    if (tn2 == null)
		    {
		    	//create new node and add it under root
			
			n2 = new Node(thirdTok, "Unknown");
			//IO.put("Node of unknown type: "+ thirdTok);
			//IO.put("firstToken := " + firstTok +" , secondToken := " +
						//secondTok + " , thirdToken := " +thirdTok);
			tn2 = new DefaultMutableTreeNode(n2);
			n2.setTreeNode(tn2);
			root.add(tn2);//add it under root
		    }
		    
		    /***********************************************************************************
		      CASE 3.3.3:     secondTok and thirdTok have corresponding nodes in the tree 
		    /***********************************************************************************/
		    //do nothing
		
		    //now create an edge from secondTok node to thirdTok node
		    
		    //NOTE: might be creating an edge from a node onto itself!!
		    
		    //edge originates in secondTok node and is directed towards thirdTok node
		    Edge e = new Edge(n1,n2,firstTok);
		    n1.addOutEdge(e);
		    n2.addInEdge(e);
		    IO.put("TAInput.java:\tEdge created from " + secondTok + " to " + thirdTok,2);
		  }
		}
		
		/************************* Read next line in input file *******************************/
		str = in.readLine();
		if (str != null) str = str.trim();
	      
	      } while ((str != null) && (!str.equals("FACT ATTRIBUTE :")));
	      
	      
	      IO.put("Reading the attributes ...",2);
	      
	      
	      // Deal with attributes here
	      if (str != null)
	      {
			str = in.readLine();
			
			if (str != null) str = str.trim();
			
			do
			{
		  		StringTokenizer attrTok = new StringTokenizer(str, " {}\t");
		  		String name = attrTok.nextToken().trim();
		  		String realName = "";
		  		//String fileName = "";
		  
		  		while (attrTok.hasMoreTokens())
		  		{
		    			String token = attrTok.nextToken();
		    			//if (token.indexOf("file=") == 0) fileName = token.substring(5);
		    			if (token.indexOf("label=") == 0) realName = token.substring(6);
		  		}
		 
		 		if (!realName.equals(""))
		  		{
		    			//change name of node here
		    			DefaultMutableTreeNode root = (DefaultMutableTreeNode)treeModel.getRoot();
		    			Enumeration allNodes = root.depthFirstEnumeration();
		    			while (allNodes.hasMoreElements())
		    			{
		      				Object i = allNodes.nextElement();
		      				DefaultMutableTreeNode j = (DefaultMutableTreeNode)i;
		      				Node n = (Node)j.getUserObject();
		      				//IO.put("@@"+n.getName()+"##"+name+"$$");
		      				
						if (n.getName().equals(name))
		      				{	
							n.setName(realName);
		      				}
		    			}	
		  		}
		  		
				str = in.readLine();
		  		
				if (str != null) str = str.trim();
			
			} while (str != null);
	      
	      }//end if
	     
	      
	      IO.put("Finished reading the input file.\n",2);
	      
	      in.close();
	    } 
	    catch(FileNotFoundException e) 
	    {
	      System.err.println(e.getMessage());
	    }
	    catch(IOException e) 
	    {
	      System.err.println(e.getMessage());
	    }
	}
}
