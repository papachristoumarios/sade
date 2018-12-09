package acdc;
import javax.swing.tree.DefaultMutableTreeNode;
import java.util.*;

public class DownInducer extends Pattern
{
	public DownInducer(DefaultMutableTreeNode _root)
	{
		super(_root);
	}
	
	public void execute() 
	{
		// Remove all but fine-grain clusters from the tree	
		Vector allNodes = allNodes(root);
		Iterator iv = allNodes.iterator();
		
		while (iv.hasNext())
		{
			Node parent = (Node) iv.next();
			DefaultMutableTreeNode tparent = (DefaultMutableTreeNode) parent.getTreeNode();
			if (parent.isCluster())
			{
				Vector subTree = nodeChildren(tparent);
				tparent.removeAllChildren();
				tparent.removeFromParent();
				Iterator is = subTree.iterator();
				boolean hasChildrenFiles = false;
				while (is.hasNext())
				{
					Node child = (Node) is.next();
					if (child.isFile())
					{
						DefaultMutableTreeNode tchild = (DefaultMutableTreeNode) child.getTreeNode();
						tchild.removeAllChildren();
						tparent.add(tchild);
						hasChildrenFiles = true;
					}
				}
				if (hasChildrenFiles) root.add(tparent);
			}
			else
			{
				tparent.removeAllChildren();
			}
		}
	}
}
