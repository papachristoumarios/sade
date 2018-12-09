package acdc;
import javax.swing.tree.DefaultMutableTreeNode;
import java.util.*;

public class UpInducer extends Pattern
{
	public UpInducer (DefaultMutableTreeNode _root)
	{
		super(_root);
	}
	
	public void execute() 
	{
		// Remove intermediate clusters from the tree
		Vector rootChildren = nodeChildren(root);
		Iterator iv = rootChildren.iterator();
		
		while (iv.hasNext())
		{
			Node parent = (Node) iv.next();
			DefaultMutableTreeNode tparent = (DefaultMutableTreeNode) parent.getTreeNode();
			Vector subTree = allNodes(tparent);
			tparent.removeAllChildren();
			Iterator is = subTree.iterator();
			while (is.hasNext())
			{
				Node child = (Node) is.next();
				if (child.isFile())
				{
					DefaultMutableTreeNode tchild = (DefaultMutableTreeNode) child.getTreeNode();
					tchild.removeAllChildren();
					tparent.add(tchild);
				}
			}
		}
	}
}
