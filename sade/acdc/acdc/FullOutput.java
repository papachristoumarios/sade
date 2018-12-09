package acdc;
import javax.swing.tree.DefaultMutableTreeNode;
import java.util.*;

public class FullOutput extends Pattern 
{
	public FullOutput (DefaultMutableTreeNode _root, String _systemName)
	{
		super(_root);
		systemName = _systemName;
	}
	
	private String systemName;
	
	public void execute() 
	{
		// Create an extra root here since OutputHandler ignores the root of the tree
		Node newDummy = new Node (systemName, "Dummy");
		DefaultMutableTreeNode newRoot = new DefaultMutableTreeNode (newDummy);
		newDummy.setTreeNode(newRoot);

		Vector rootChildren = nodeChildren(root);
		Iterator irC = rootChildren.iterator();
		while (irC.hasNext())
		{
			Node n = (Node) irC.next();
			DefaultMutableTreeNode curr = n.getTreeNode();
			newRoot.add(curr);
		}
		root.add(newRoot);
	}
}