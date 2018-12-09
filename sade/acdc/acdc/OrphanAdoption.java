package acdc;
import java.util.Enumeration;
import java.util.HashSet;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.Vector;

import javax.swing.tree.DefaultMutableTreeNode;

/** 
 * This pattern finds and moves children of the root node which are not
 * clusters under the appropriate adoptive cluster-node.
 * An orphan would be placed under the cluster-node with
 * the largest number of children which point to the orphan. 
 * 
 * Tie-breakers are solved by checking the targets of the orphan.
 * 
 * If cluster-nodes A and B are competing for the orphan, that
 * which has the largest number of children being targets of the 
 * orphan, wins it.
 *
 */
public class OrphanAdoption extends Pattern 
{
	public OrphanAdoption(DefaultMutableTreeNode _root)
	{
		super(_root);
		name = "Orphan Adoption";
	}

	public void execute() 
	{
		Vector vModified = new Vector();
		Vector vAdopted;		
		// Run oneRoundForward as many times as the #orphans is decreasing 
		vAdopted = manyRoundsForward();
		
		int on, prevon;
		on = orphanNumber();
		prevon = on + 1;
		while(on < prevon)
		{
			IO.put("Orphan Number: " + on,2);
			prevon = on;
			vAdopted = oneRoundReverse();
			vModified.addAll(vAdopted);
			if (orphanNumber() > 0)
			{
				vAdopted = manyRoundsForward();
				vModified.addAll(vAdopted);
			}
			on = orphanNumber();
		}
		induceEdges(vModified,root);
	}
	
	public Vector oneRoundReverse()
	{
		Vector vReturn = new Vector();
		Vector vRootChildren = nodeChildren(root);
		// Keeps the cluster-nodes which are competing for this orphan 
		Hashtable ht = new Hashtable(10000);
	
	for(int j=0; j<vRootChildren.size();j++)
	{
	   Node ncurr = (Node)vRootChildren.elementAt(j);
	   DefaultMutableTreeNode curr = (DefaultMutableTreeNode)ncurr.getTreeNode();
                              	
		if(!ncurr.isCluster())
		{	
		ht = new Hashtable(10000);
		IO.put("ROA:\torphan =: "+ ncurr.getName(),2);

		//a set of the nodes to which the current orphan points to
		HashSet targets = ncurr.getTargets();
		//if(targets.isEmpty())
			//IO.put("orphan =:"+ncurr.getName()+" has NO TARGETS!");	
		
		Iterator itargets = targets.iterator();
		while (itargets.hasNext())
		{
			Node ncurr_target = (Node)(itargets.next());
			DefaultMutableTreeNode curr_target = 
				(DefaultMutableTreeNode)(ncurr_target.getTreeNode());
			    		
			double counter = 0;
		    
			 /**********************************************************************************    
		      
			  NOTE: retain only targets of the orphan which are clusters <-- only the cluster
					which is lowest in the tree should adopt the orphan,
			 *********************************************************************************/
		    
			//ignore root and its children  as targets of the orphan;
			//also ignore targets of the orphan which are clusters
			if(curr_target.getLevel()>1 && !ncurr_target.isCluster())
			{
			
			
			//IO.put("Rorphan := "+ ncurr.getName() +":::::::::::::: target =: " 
															   //+ncurr_target.getName());
			
			//the parent of this target is competing for the orphan  
			DefaultMutableTreeNode parent =(DefaultMutableTreeNode)curr_target.getParent();
			Node nparent = (Node)parent.getUserObject();			
			//IO.put("::::::: whose parent is :=  ");
			//if parent is orphan or root, do nothing
			if(nparent.getName().equalsIgnoreCase(ncurr.getName()) || nparent.getName().equalsIgnoreCase("ROOT"))
					;
					//IO.put("\nParent of target of orphan " + ncurr.getName() +
						//" is Root or the orphan itself.\n");
			else
			{
				boolean stop = false;
				while(!stop && !nparent.isCluster())
				{
					parent = (DefaultMutableTreeNode)parent.getParent();
					nparent = (Node)parent.getUserObject();
					
					//parent of the source is root or is the orphan
					if(nparent.getName().equalsIgnoreCase(ncurr.getName()) ||
										   nparent.getName().equalsIgnoreCase("ROOT"))
					{
						
						stop = true;
					}
				}
			}
			
			if(nparent.isCluster())
			{
				//dvalues, ivalues, ivalue --> needed for printing only
				//Collection dvalues;
				//Vector ivalues;
				//Double ivalue;
				
				//IO.put(nparent.getName());
				
				//Case1: parent already in the hashtable 
				if(ht.containsKey(nparent))
				{  
				   //counter value get incremented by one unit
					Double i = (Double)ht.get(nparent);
				    
					//IO.put(", iCounter:= " + i);
				    
					counter = i.doubleValue();
					counter++;   
					//remove source with old counter value from the hashtable
					ht.remove(nparent);
					//add the source back to the hashtable with the updated counter value
					ht.put(nparent, new Double(counter));
				    
					//IO.put(", fCounter not new:= "+ counter);
				    
					/*
					IO.put("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^");
					dvalues = ht.values();
					ivalues = new Vector(dvalues);
					for(int j=0; j<ivalues.size(); j++)
					{
						ivalue = (Double)ivalues.elementAt(j);
						IO.put("Value of Hashtable **** " + ivalue.doubleValue());
					}
					IO.put("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^");
					*/
				}
				//Case2: parent was not in the hashtable 
				else
				{   
						counter = 0;
					
					HashSet c_targets = new HashSet();
					Enumeration ps = parent.breadthFirstEnumeration();
					while(ps.hasMoreElements())
					{
						DefaultMutableTreeNode ps_curr = (DefaultMutableTreeNode)ps.nextElement();
						Node nps_curr = (Node)ps_curr.getUserObject();
						c_targets= nps_curr.getTargets();
						if(c_targets.contains(ncurr))
						{	counter = counter + 0.000001;
							//IO.put(", Counter:= "+ counter);
						}	
					}
					
					//add parent to the hashtable with a counter value incremented by one more unit
					ht.put(nparent, new Double(++counter));
					//IO.put(", Counter:= "+ counter);
					
					/*
					IO.put("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^");
					dvalues = ht.values();
					ivalues = new Vector(dvalues);
						for(int i=0; i<ivalues.size(); i++)
						{
							ivalue = (Double)ivalues.elementAt(i);
							IO.put("Value of Hashtable **** " + ivalue.doubleValue());
						}
						IO.put("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^");
					*/
				}
			}
					
				}
				
		}// end while
		
		if(ht.isEmpty())
			IO.put("\tNOT\t adopted",2);
		//the hashtable now contains all the candidate nodes for adopting the orphan
		//the node in the hashtable with the highest counter value will get the orphan
		if(!ht.isEmpty())
		{	
			double max_value = 0;
			Node max_key = new Node("faraz","oana");
		    
			/*
			Collection cvalues = ht.values();
			Vector values = new Vector(cvalues);
			for(int i=0; i<values.size(); i++)
			{
				Double value = (Double)values.elementAt(i);
				IO.put("Value of Hashtable **** " + value.doubleValue());
			}
			*/
		    
			Enumeration keys = ht.keys();
			while (keys.hasMoreElements())
			{
			Node curr_key =  (Node)keys.nextElement();
			//IO.put("Hashtable contains: ");
			//curr_key.print();
			
			Double curr_value = (Double)ht.get(curr_key);
			//IO.put(", Value := " + curr_value.doubleValue());
			
			
			if(curr_value.doubleValue() >= max_value)
			{
				max_value = curr_value.doubleValue() ;
				max_key = curr_key;
			}
		    	
			}
		    
			DefaultMutableTreeNode max = (DefaultMutableTreeNode)(max_key.getTreeNode());
			max.add(curr);
		 
			Enumeration emax = curr.breadthFirstEnumeration();
			while(emax.hasMoreElements())
			{
				DefaultMutableTreeNode ec = (DefaultMutableTreeNode)emax.nextElement();
			if(!vReturn.contains((Node)ec.getUserObject()))
				vReturn.add((Node)ec.getUserObject());
			}
		  
			IO.put("\twas adopted by ***\t" + max_key.getName(),2);
		   
		}
		}// end if     
	}// end while		
	
	return vReturn;
	}
	
	public Vector manyRoundsForward()
	{
		Vector result = new Vector();
		Vector vAdopted;		
		// Run oneRoundForward as many times as the #orphans is decreasing 
		do
		{
			vAdopted = oneRoundForward();
			IO.put("Before "+vAdopted.size(),2);
			result.addAll(vAdopted);
			IO.put("After "+vAdopted.size()+"",2);
		}
		while(vAdopted.size() > 0);
		return result;
	}
	
	public Vector oneRoundForward ()
	{
		Vector vReturn = new Vector();
		//vector will contain the orphans adopted
		Vector vRootChildren = nodeChildren(root);

		// Hashtable keeps track of the nodes competing for the current orphan 
		Hashtable ht = new Hashtable(10000);

		for (int j = 0; j < vRootChildren.size(); j++) 
		{
			Node ncurr = (Node) vRootChildren.elementAt(j);
			DefaultMutableTreeNode curr = (DefaultMutableTreeNode) ncurr.getTreeNode();

			if (!ncurr.isCluster()) 
			{
				//begin with an empty hashtable for each orphan
				ht = new Hashtable(10000);
				IO.put("OA:\torphan  =: " + ncurr.getName(), 2);

				//sources = set of nodes which point to the current orphan 
				HashSet sources = ncurr.getSources();
				//ncurr.printSources();
				//if(sources.isEmpty())
				//IO.put("orphan =:"+ncurr.getName()+" has NO SOURCES!");
				Iterator isources = sources.iterator();
				//iterate through the sources

				while (isources.hasNext()) 
				{
					Node ncurr_source = (Node) (isources.next());
					//IO.put("\tSource =: " +ncurr_source.getName());
					DefaultMutableTreeNode curr_source =
						(DefaultMutableTreeNode) (ncurr_source.getTreeNode());

					double counter = 0;

					/**********************************************************************************    
					  
					  NOTE: retain only sources of the orphan which are clusters <-- only the cluster
					        which is lowest in the tree should adopt the orphan,
					 *********************************************************************************/

					//ignore root and its children  as sources of the orphan;

					//      --> we ignore sources of the orphan which are clusters
					if (curr_source.getLevel() > 1 && !ncurr_source.isCluster()) 
					{
						//IO.put("orphan := "+ ncurr.getName() +":::::::::::::: source =: " +ncurr_source.getName());

						//the parent of this source is competing for the orphan  
						DefaultMutableTreeNode parent =
							(DefaultMutableTreeNode) curr_source.getParent();
						Node nparent = (Node) parent.getUserObject();
						//IO.put("::::::: whose parent is :=  ");

						//if parent is orphan or root, do nothing
						if (nparent.getName().equalsIgnoreCase(ncurr.getName())
							|| nparent.getName().equalsIgnoreCase("ROOT"));
						else {
							boolean stop = false;
							while (!stop && !nparent.isCluster()) {
								parent =
									(DefaultMutableTreeNode) parent.getParent();
								nparent = (Node) parent.getUserObject();

								//parent of the source is root or is the orphan
								if (nparent.getName().equalsIgnoreCase(ncurr.getName())
									|| nparent.getName().equalsIgnoreCase("ROOT")) {

									stop = true;
								}
							}
						}

						if (nparent.isCluster()) {
							//dvalues, ivalues, ivalue --> needed for printing only
							//Collection dvalues;
							//Vector ivalues;
							//Double ivalue;

							//IO.put(nparent.getName());
							//Case1: parent already in the hashtable 
							if (ht.containsKey(nparent)) {
								//counter value get incremented by one unit
								Double i = (Double) ht.get(nparent);
								//IO.put(", iCounter:= " + i);
								counter = i.doubleValue();
								counter++;
								//remove source with old counter value from the hashtable
								ht.remove(nparent);
								//add the source back to the hashtable with the updated counter value
								ht.put(nparent, new Double(counter));
								//IO.put(", fCounter not new:= "+ counter);

								/*
								IO.put("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^");
								dvalues = ht.values();
								ivalues = new Vector(dvalues);
								for(int j=0; j<ivalues.size(); j++)
								{
									ivalue = (Double)ivalues.elementAt(j);
									IO.put("Value of Hashtable **** " + ivalue.doubleValue());
								}
								IO.put("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^");
								*/
							}
							//Case2: parent not in the hashtable
							else {
								counter = 0;
								HashSet c_sources = new HashSet();
								Enumeration ps =
									parent.breadthFirstEnumeration();
								ps.nextElement();
								//don't count the parent itself which surely points to curr due to edge induction
								while (ps.hasMoreElements()) {
									DefaultMutableTreeNode ps_curr =
										(DefaultMutableTreeNode) ps
											.nextElement();
									Node nps_curr =
										(Node) ps_curr.getUserObject();
									c_sources = nps_curr.getSources();
									if (c_sources.contains(ncurr)) {
										counter = counter + 0.000001;
										//IO.put(", Counter:= "+ counter);
									}
								}

								//add parent to the hashtable with a counter value incremented by one more unit
								ht.put(nparent, new Double(++counter));
								//IO.put(", Counter:= "+ counter);

								/*
								IO.put("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^");
								dvalues = ht.values();
								ivalues = new Vector(dvalues);
								    for(int i=0; i<ivalues.size(); i++)
								    {
										ivalue = (Double)ivalues.elementAt(i);
										IO.put("Value of Hashtable **** " + ivalue.doubleValue());
								    }
								    IO.put("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^");
								*/
							}
						}
						//else
						//IO.put("");		
					}

				} // end while

				if (ht.isEmpty())
					IO.put("\tNOT\t adopted", 2);
				//the hashtable now contains all the candidate nodes for adopting the orphan
				//the node in the hashtable with the highest value will get the orphan
				if (!ht.isEmpty()) {
					double max_value = 0;
					Node max_key = new Node("faraz", "oana");

					/*
					Collection cvalues = ht.values();
					Vector values = new Vector(cvalues);
					for(int i=0; i<values.size(); i++)
					{
						Double value = (Double)values.elementAt(i);
						IO.put("Value of Hashtable **** " + value.doubleValue());
					}
					*/

					Enumeration keys = ht.keys();
					while (keys.hasMoreElements()) {
						Node curr_key = (Node) keys.nextElement();
						//IO.put("Hashtable contains: ");
						//curr_key.print();

						Double curr_value = (Double) ht.get(curr_key);
						//IO.put(", Value := " + curr_value.doubleValue());

						if (curr_value.doubleValue() >= max_value) {
							max_value = curr_value.doubleValue();
							max_key = curr_key;
						}

					}

					DefaultMutableTreeNode max =
						(DefaultMutableTreeNode) (max_key.getTreeNode());
					max.add(curr);

					Enumeration emax = curr.breadthFirstEnumeration();
					while (emax.hasMoreElements()) {
						DefaultMutableTreeNode ec =
							(DefaultMutableTreeNode) emax.nextElement();
						if (!vReturn.contains((Node) ec.getUserObject()))
							vReturn.add((Node) ec.getUserObject());
					}

					IO.put("\twas adopted by ***\t" + max_key.getName(), 2);

				}
			} // end if     
		} // end while

		return vReturn;
	} //end execute
} //end class
