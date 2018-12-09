package acdc;
import java.util.Iterator;
import java.util.Vector;

import javax.swing.tree.DefaultMutableTreeNode;

/**
* This pattern puts together all orphans under one cluster node named
* "orphanContainer", which in turn is inserted under the root of the tree.
*/
public class ClusterLast extends Pattern {
	public ClusterLast(DefaultMutableTreeNode _root) {
		super(_root);
		name = "Cluster Last";
	}

	public void execute() {
		Vector vModified = new Vector();

		if (orphanNumber() != 0) {
			IO.put("Clustering leftover nodes",2);
			// Create a node of type Subsystem which will contain all the remaining unclustered orphans 
			Node nOrphanContainer = new Node("orphanContainer.ss", "Subsystem");
			DefaultMutableTreeNode orphanContainer = new DefaultMutableTreeNode(nOrphanContainer);
			nOrphanContainer.setTreeNode(orphanContainer);
			root.add(orphanContainer);

			Vector allOrphans = orphans();
			Iterator iaO = allOrphans.iterator();

			while (iaO.hasNext())
			{
				Node ncurr = (Node) iaO.next();
				// Change this to an iterator
				//for (int i = 0; i < orphanNumber(); i++) {
				//Node ncurr = (Node) orphans().elementAt(i);
				DefaultMutableTreeNode curr = (DefaultMutableTreeNode) (ncurr.getTreeNode());

				if (!ncurr.isCluster())
				{
					orphanContainer.add(curr);
					IO.put("contain\t\t" + nOrphanContainer.getName() + "\t" + ncurr.getName(),	2);

/* Commented this out. Why do we need to induce edges at this point?
   Uncomment the induceEdges line below, if we need to bring this back in
   
					vModified.add(ncurr);

					Enumeration ecurr = curr.breadthFirstEnumeration();
					while (ecurr.hasMoreElements())
					{
						DefaultMutableTreeNode em = (DefaultMutableTreeNode) ecurr.nextElement();
						vModified.add((Node) em.getUserObject());
					}

					Enumeration emax = curr.breadthFirstEnumeration();
					while (emax.hasMoreElements()) {
						DefaultMutableTreeNode ec =
							(DefaultMutableTreeNode) emax.nextElement();
						vModified.add((Node) ec.getUserObject());
					}
*/
				}
			} // end while
		} //end if

		//induceEdges(vModified, root);
	} //end clusterLast
}
