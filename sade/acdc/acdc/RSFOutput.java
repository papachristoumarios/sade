package acdc;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Enumeration;

import javax.swing.tree.DefaultMutableTreeNode;

/**
* This class has one method which creates an RSF file.
* 
* The string representation of the output is of the format: 
*
* contain parent_node node
*
*/
public class RSFOutput implements OutputHandler 
{
	public void writeOutput(String outputName, DefaultMutableTreeNode root) 
	{
		PrintWriter out = null;
		try 
		{
			out = new PrintWriter(new BufferedWriter(new FileWriter(outputName)));
		} 
		catch (IOException e) 
		{
			System.err.println(e.getMessage());
		}

		Node ncurr, nj, ni, np;
		DefaultMutableTreeNode curr, i, j, pi;

		Enumeration allNodes = root.breadthFirstEnumeration();

		// Avoid output for the root node
		i = (DefaultMutableTreeNode) allNodes.nextElement();

		while (allNodes.hasMoreElements()) 
		{
			i = (DefaultMutableTreeNode) allNodes.nextElement();

			ni = (Node) i.getUserObject();

			pi = (DefaultMutableTreeNode) i.getParent();

			np = (Node) pi.getUserObject();

			if (pi != root) out.println("contain " + np.getName() + " " + ni.getName());
		}
		out.close();
	}
}