package acdc;
import java.util.*;
import javax.swing.tree.*;

public abstract class Pattern {
	public Pattern(DefaultMutableTreeNode _root)
	{
		root = _root;
		name = "";
	}
	
	protected DefaultMutableTreeNode root;
	
	protected String name;
	
	public String getName()
	{
		return name;
	}

	protected abstract void execute();

	protected Vector nodeChildren(DefaultMutableTreeNode node) 
	{
		Vector result = new Vector();
		Enumeration children = node.children();
		while (children.hasMoreElements()) 
		{
			DefaultMutableTreeNode curr2 = (DefaultMutableTreeNode) children.nextElement();
			Node ncurr2 = (Node) curr2.getUserObject();
			result.add(ncurr2);
		}
		return result;
	}
	
	protected Vector orphans()
	{
		Vector result = new Vector();
		Vector rootChildren = nodeChildren(root);
		Iterator iv = rootChildren.iterator();

		while (iv.hasNext())
		{
			Node curr = (Node) iv.next();
			if (!curr.isCluster())
				result.add(curr);
		}
		return result;
	}

	protected int orphanNumber()
		{
			Vector rootChildren = nodeChildren(root);
			Iterator iv = rootChildren.iterator();
			int count = 0;
			while (iv.hasNext())
			{
				Node curr = (Node) iv.next();
				if (!curr.isCluster())
					count ++;
			}
			return count;
		}

	public static Vector allNodes(DefaultMutableTreeNode root)
	{
		Vector result = new Vector(); // will contain all nodes in the tree
		Enumeration treeNodes = root.breadthFirstEnumeration();
		// The first node in the enumeration is the root. We skip it over.
		DefaultMutableTreeNode curr = (DefaultMutableTreeNode) treeNodes.nextElement();
		while(treeNodes.hasMoreElements())
		{
			curr = (DefaultMutableTreeNode)treeNodes.nextElement();
			Node ncurr = (Node)curr.getUserObject();
			result.add(ncurr);
		}
		return result;
	}
	
	public static void induceEdges(Vector v, DefaultMutableTreeNode root) 
	{
		IO.put("The following " + v.size() + " nodes were selected for edge induction", 2);
		for (int m = 0; m < v.size(); m++)
		{
			Node ncurr = (Node) v.elementAt(m);
			IO.put(ncurr.getName(), 2);
			HashSet outNodes = (HashSet) ncurr.getTargets().clone();
			//IO.put("\n");
			//traverse the set of target nodes of the current node
			Iterator ioN = outNodes.iterator();
			while (ioN.hasNext()) {
				//traverse the nodes from the root to the current   
				//target node creating edges 
				Node across = (Node) ioN.next();
				DefaultMutableTreeNode tacross = across.getTreeNode();
				TreeNode[] path = tacross.getPath();
				for (int i = 0; i < path.length; i++) {
					TreeNode k = path[i];
					DefaultMutableTreeNode j = (DefaultMutableTreeNode) k;
					Node nj = (Node) j.getUserObject();
					//IO.put("EdgeInduction.java\t\tTarget " + nj.getName());
					//don't create induced edges for the root or circular edges 
					if (!j.isRoot()) {
						Edge e = new Edge(ncurr, nj, "induced");
						IO.put("\tInduced edge from "	+ ncurr.getName() + " to " + nj.getName(), 2);
						nj.addInEdge(e);
						ncurr.addOutEdge(e);
					}
				}
			}
		}

		for (int j = 0; j < v.size(); j++) {

			Node ncurr2 = (Node) v.elementAt(j);
			IO.put(ncurr2.getName(), 2);
			//keep a set of the sources nodes of the current node
			HashSet outNodes2 = (HashSet) ncurr2.getSources().clone();

			//traverse the set of target nodes of the current node
			Iterator ioN2 = outNodes2.iterator();
			while (ioN2.hasNext()) {
				//IO.put("\n");
				//traverse the nodes from the root to
				//the current target node creating edges
				Node across2 = (Node) ioN2.next();
				DefaultMutableTreeNode tacross2 = across2.getTreeNode();
				TreeNode[] path2 = tacross2.getPath();
				for (int i = 0; i < path2.length; i++) {
					TreeNode k2 = path2[i];
					DefaultMutableTreeNode j2 = (DefaultMutableTreeNode) k2;
					Node nj2 = (Node) j2.getUserObject();
					//IO.put("EdgeInduction.java\t\tSource " + nj2.getName());
					//current node is in the path of current source
					//therefore don't create any edges
					//if(nj2.getName().equalsIgnoreCase(ncurr.getName()))
					//{

					//}else{
					//don't create induced edges for
					//the root
					if (!j2.isRoot()) {
						Edge e2 = new Edge(nj2, ncurr2, "induced");
						IO.put("\tInduced edge from " + nj2.getName() + " to " + ncurr2.getName(), 2);
						nj2.addOutEdge(e2);
						ncurr2.addInEdge(e2);
					}
				}
			}
		}
	}
}
