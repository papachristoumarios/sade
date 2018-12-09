package acdc;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Enumeration;
import java.util.HashSet;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.Vector;
import javax.swing.tree.DefaultMutableTreeNode;

/**
 * @author V. Tzerpos
 *
 * Clusters the children of the root based on their dependencies
 */
public class SubGraph extends Pattern {
	private int clusterSize;

	public SubGraph(DefaultMutableTreeNode _root, int size) {
		super(_root);
		clusterSize = size;
		name = "Subgraph Dominator";
	}

	public void execute() {
		Vector vModified = new Vector();
		Vector vRootChildren = nodeChildren(root);

		//************************************************************************
		// Note: The nodes to be clustered are the children of the root only. 
		//       Their corresponding subtree should not be modified!             
		//************************************************************************

		HashSet setOfTargets = new HashSet();

		//put nodes to be clustered together with their corresponding number of targets in a HashTable
		Hashtable ht = new Hashtable(10000);

		int counter = 0; // keeps track of #targets per node

		Iterator ivRC = vRootChildren.iterator();
		while (ivRC.hasNext())
		{
			Node ncurr = (Node) ivRC.next();
			setOfTargets = new HashSet(); //reset

			setOfTargets.add((DefaultMutableTreeNode) ncurr.getTreeNode());
			setOfTargets = findTargets(setOfTargets, vRootChildren);

			counter = 0; //reset

			Iterator ihs = setOfTargets.iterator();
			//count only targets which are children of root
			while (ihs.hasNext()) {
				DefaultMutableTreeNode c = (DefaultMutableTreeNode) ihs.next();
				Node n = (Node) c.getUserObject();

				if (vRootChildren.contains(n)) {
					//IO.put(n.getName()+" is in vRootChildren");
					counter++;
				}
			}
			ht.put(ncurr, new Integer(counter));
		}

		//sort ht in increasing order

		ArrayList my_array = new ArrayList();
		for (Enumeration e = ht.keys(); e.hasMoreElements();) {
			Node curr_key = (Node) e.nextElement();
			Integer curr_value = (Integer) ht.get(curr_key);

			// build a sortable object with the two pieces of information
			Sortable s_before = new Sortable(curr_value, curr_key);

			// add the sortable object to the sarray
			my_array.add(s_before);
		}
		Collections.sort(my_array);

		for (int i = 0; i < my_array.size(); i++) {

			Sortable s_print = (Sortable) my_array.get(i);

			Node object_key = (Node) s_print.getObject();

			Integer integer_object = (Integer) s_print.getKey();

			IO.put("Node = " + object_key.getName()	+
			       " , Type := "	+ object_key.getType() +
			       " , Targets = " + integer_object, 2);

		}

		Node tentativeDominator;
		int next_index = 0;
		boolean found;
		
		// This is where the big loop begins
		
		while (!ht.isEmpty()) {
			//some nodes (identified below as covered set nodes) might be removed from
			//the hashtable so we want to make sure that our ArrayList is also updated
			do {
				Sortable s_after = (Sortable) my_array.get(next_index++);
				tentativeDominator = (Node) s_after.getObject();
				//while hashtable doesn't contain it, skip over current node to the next one
				if (ht.containsKey(tentativeDominator))
					found = true;
				else
					found = false;
			} while (!found);

			DefaultMutableTreeNode tentativeDominatorTreeNode = (DefaultMutableTreeNode) (tentativeDominator.getTreeNode());

			IO.put("**************************", 2);
			IO.put("Dominator " + tentativeDominator, 2);
			HashSet cS = coveredSet(tentativeDominatorTreeNode, vRootChildren);
			if (cS.size() == 1)
			{
				ht.remove(tentativeDominator);
			}
			else //coveredSet returned tentativeRoot and its set of dominated nodes
			{
				// max cluster size allowed is clusterSize!!

				DefaultMutableTreeNode curr_cS;
				Node ncurr_cS;
				if (cS.size() < clusterSize)
				{
					Iterator ic = cS.iterator();
					while (ic.hasNext())
					{
						curr_cS = (DefaultMutableTreeNode) ic.next();
						ncurr_cS = (Node) curr_cS.getUserObject();
						//IO.put("Covered Set Node ***" + ncurr_cS.getName() + " ,Type := " +
						// ncurr_cS.getType() + " was removed from hashtable!!!");
						ht.remove(ncurr_cS);
					}
				}
				else //if cS has more than clusterSize elements, attempt deeper clustering
				{
					ht.remove(tentativeDominator);
				}

				// Create a new subsystem node
				Node ssNode = new Node(tentativeDominator.getBaseName() + ".ss", "Subsystem");
				if (!vModified.contains(ssNode))
				{
					vModified.add(ssNode);
				}

				IO.put("Cluster Node " + ssNode.getName() + " was created and contains :", 2);

				DefaultMutableTreeNode ssTreeNode = new DefaultMutableTreeNode(ssNode);
				ssNode.setTreeNode(ssTreeNode);

				// Find the most immediate common ancestor of all elements in the covered set
				Iterator icS = cS.iterator();
				DefaultMutableTreeNode ancestor = (DefaultMutableTreeNode) icS.next();
				ancestor = (DefaultMutableTreeNode) ancestor.getSharedAncestor((DefaultMutableTreeNode) icS.next());
				while (icS.hasNext())
				{
					ancestor = (DefaultMutableTreeNode) ancestor.getSharedAncestor((DefaultMutableTreeNode) icS.next());
				}

				// Insert the new node just below the ancestor
				Iterator ics2 = cS.iterator();
				HashSet nodesToMove = new HashSet();

				IO.put("Ancestor :=  " + ((Node) (ancestor.getUserObject())).getName(), 2);
				int numOfElementsInPath = 0;
				boolean continueLoop = true;
				while (ics2.hasNext() && continueLoop) {

					DefaultMutableTreeNode nnn = (DefaultMutableTreeNode) ics2.next();
					Enumeration path = nnn.pathFromAncestorEnumeration(ancestor);
					numOfElementsInPath = 0;
					while (path.hasMoreElements()) {
						path.nextElement();
						numOfElementsInPath++;
					}
					//IO.put("numOfElementsInPath := " 
					// + numOfElementsInPath);
					//if ancestor belongs to covered set,only ancestor should be moved
					if (numOfElementsInPath == 1) {
						nodesToMove.clear();
						nodesToMove.add(ancestor);
						continueLoop = false;
						IO.put("Ancestor belongs to the covered set!", 2);
					} else {
						path = nnn.pathFromAncestorEnumeration(ancestor);

						//firstNode is same as ancestor!
						DefaultMutableTreeNode firstNode =
							(DefaultMutableTreeNode) path.nextElement();

						DefaultMutableTreeNode secondNode =
							(DefaultMutableTreeNode) path.nextElement();
						nodesToMove.add(secondNode);
					}

				}

				//new node contains all the nodes in covered set and others too
				Iterator intm = nodesToMove.iterator();
				while (intm.hasNext()) {
					DefaultMutableTreeNode nextToMove =
						(DefaultMutableTreeNode) intm.next();
					if (!nextToMove.equals(ssTreeNode))
						ssTreeNode.add(nextToMove);

					//there are no outside sources for coveredSet nodes, threfore edgeInduction is only needed for the 
					//newly created cluster node 

					Enumeration ecurr = nextToMove.breadthFirstEnumeration();
					while (ecurr.hasMoreElements()) {

						DefaultMutableTreeNode em =
							(DefaultMutableTreeNode) ecurr.nextElement();
						if (!vModified.contains((Node) em.getUserObject()))
							vModified.add((Node) em.getUserObject());
					}

					IO.put(" Moved:\t" + ((Node) (nextToMove.getUserObject())).getName(), 2);
				}

				if (ancestor == root) {
					ancestor.add(ssTreeNode);

				} else {
					//only child is the ancestor
					if (ssTreeNode.equals(ancestor)) {
						IO.put("Opa", 2);

						//DefaultMutableTreeNode parentOfAncestor = 
						//(DefaultMutableTreeNode)ancestor.getParent();
						//IO.put("Parent of Ancestor :=  " 
						//+ ((Node)(parentOfAncestor.getUserObject())).getName()) ;

						// if ancestor belongs to covered set, former parent 
						//of ancestor (current parent of ancestor is ssTreeNode) 
						// should become parent of ssTreeNode
						//parentOfAncestor.add(ssTreeNode);
					} else {
						ancestor.add(ssTreeNode);

					}

				}

			} //end else
			//loop++;
		} //end while
		//return -1;
		induceEdges(vModified, root);
	} //end execute

	static void printCoveredSet(DefaultMutableTreeNode domin, Vector vTree) {
		IO.put(
			"**************************************************************",
			2);
		HashSet cS = coveredSet(domin, vTree);
		Iterator icS = cS.iterator();
		while (icS.hasNext()) {
			DefaultMutableTreeNode curr = (DefaultMutableTreeNode) icS.next();
			Node ncurr = (Node) curr.getUserObject();
			IO.put(
				"\tCovered Set Node: **** "
					+ ncurr.getName()
					+ " , Type := "
					+ ncurr.getType(),
				2);
		}

		HashSet tS = findTargets(cS, vTree);
		Iterator itS = tS.iterator();
		while (itS.hasNext()) {
			DefaultMutableTreeNode curr1 = (DefaultMutableTreeNode) itS.next();
			Node ncurr1 = (Node) curr1.getUserObject();
			IO.put(
				"\t** Target of covered set:= "
					+ ncurr1.getName()
					+ " , Type := "
					+ ncurr1.getType(),
				2);

			HashSet sS = findSources(curr1, vTree);
			Iterator isS = sS.iterator();
			while (isS.hasNext()) {
				DefaultMutableTreeNode curr2 =
					(DefaultMutableTreeNode) isS.next();
				Node ncurr2 = (Node) curr2.getUserObject();
				IO.put(
					"\t\tIts source := "
						+ ncurr2.getName()
						+ " , Type := "
						+ ncurr2.getType(),
					2);
			}
		}
	}

	/**
	* Returns the HashSet containing the passed arg, called "dominator node", and 
	* the set of its dominated nodes, N = n(i), i:1,2,...m,  which have 
	* the following properties:
	*
	* 1. there exists a path from tentativeRoot to every n(i)
	* 2. for any node v such that there exists a path from v to any n(i), either 
	*    tentativeRoot is in that path or v is one of n(i)
	*/
	private static HashSet coveredSet(
		DefaultMutableTreeNode tentativeRoot,
		Vector vTree) {
		HashSet result = new HashSet();
		result.add(tentativeRoot);

		HashSet covered, falseOnes, fathers, both;

		do {
			covered = findTargets(result, vTree);
			covered.removeAll(result);
			falseOnes = new HashSet();
			do {
				both = (HashSet) covered.clone();
				both.addAll(result);
				Iterator ic = covered.iterator();
				while (ic.hasNext()) {
					DefaultMutableTreeNode curr =
						(DefaultMutableTreeNode) ic.next();
					fathers = findSources(curr, vTree);
					if (!both.containsAll(fathers))
						falseOnes.add(curr);
				}

			}
			while (covered.removeAll(falseOnes));
			// will exit if covered doesn't change
		}
		while (result.addAll(covered)); // will exit if result doesn't change
		return result;
	}

	/**
	* Returns a HashSet containing the target nodes of all the
	* items in the passed HashSet parameter.
	*/
	private static HashSet findTargets(
		HashSet source,
		Vector vRootChildren) // was vTree
	{

		HashSet allTargets = new HashSet();

		//iterate thorough the passed HashSet    
		Iterator iS = source.iterator();
		while (iS.hasNext()) {
			DefaultMutableTreeNode curr = (DefaultMutableTreeNode) iS.next();
			Node ncurr = (Node) curr.getUserObject();

			//get the targets of the current node in the iteration      
			HashSet targets = ncurr.getTargets();

			//iterate through these targets adding each to the HashSet 'targets'
			Iterator iT = targets.iterator();
			while (iT.hasNext()) {
				Node n = (Node) iT.next();

				if (vRootChildren.contains(n)) // was !vTree
					{
					DefaultMutableTreeNode t = n.getTreeNode();
					allTargets.add(t);
				}
			}
		}
		return allTargets;
	}

	/**
	* Returns a HashSet containing the sources of the passed node parameter.
	*/
	private static HashSet findSources (DefaultMutableTreeNode target, Vector vRootChildren)
	{
		HashSet allSources = new HashSet();

		//get sources of the passed node
		Node ntarget = (Node) target.getUserObject();
		HashSet sources = ntarget.getSources();

		//iterate through the sources of the passed node
		//and add them to the HashSet called 'sources'
		Iterator iS = sources.iterator();
		while (iS.hasNext()) {
			Node n = (Node) iS.next();
			if (vRootChildren.contains(n))
				{
				DefaultMutableTreeNode t = n.getTreeNode();
				allSources.add(t);
			}
		}
		return allSources;
	}
}