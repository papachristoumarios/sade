package acdc;
/**
* This class encapsulates information about an Edge object.
* It provides get and set methods for the attributes of this Edge object.
*/
public class Edge 
{
  // Instance variables
  private Node source;
  private Node target;
  private String type;
  private int  weight;
  
 /**
  * Creates an edge initialized with the passed parameters as its source, target,
  * respectively type.
  * @param source   the node which acts as the source of this object
  * @param target   the node which acts as the target of this object
  * @param type	    the type of this object
  */ 
  public Edge(Node source, Node target, String type) 
  {
    this.source = source;
    this.target = target;
    this.type = type;
    weight = 1;
  }
  
 /**
  * Creates an edge initialized with the passed parameters as its source, target,
  * type, respectively weight.
  * @param source   the node which acts as the source of this object
  * @param target   the node which acts as the target of this object
  * @param type	    the type of this object
  * @param weight   the weight of this object 
  */
  public Edge(Node source, Node target, String type, int weight) 
  {
    this.source = source;
    this.target = target;
    this.type = type;
    this.weight = weight;
  }
  
  /**
   * Returns the Node from where <code>this</code> edge originates
   * @return the Node from where this edge originates
   */
   public Node getSource() { return source; }
   
  /**
   * Returns the name of the Node from where <code>this</code> edge originates
   * @return the name of the Node from where this edge originates
   */
   public String getSourceName() { return source.getName(); }
   
  /**
   * Returns the Node towards which <code>this</code> edge is directed
   * @return the Node towards which this edge is directed
   */
   public Node getTarget() { return target; }
   
  /**
   * Returns the name of the Node towards which <code>this</code> edge is directed
   * @return the name of the Node towards which this edge is directed
   */
   public String getTargetName() { return target.getName(); }
   
  /**
   * Returns <code>this</code>  edge's type
   * @return the type of this object
   */
   public String getType() { return type; }
   
  /**
   * Returns <code>this</code> edge's weight value
   * @return the weight value of this edge
   */
   public int getWeight()  { return weight; }
   
  /**
   * Sets the source of <code>this</code> edge 
   * @param source the Node from which this edge originates
   */
   public void setSource(Node source) { this.source = source; }
   
  /**
   * Sets the target of <code>this</code> edge 
   * @param target the Node towards which this edge is directed
   */
   public void setTarget(Node target) { this.target = target; }
   
  /**
   * Sets the type of <code>this</code> edge 
   * @param type the type of this edge
   */
   public void setType(String type) { this.type = type; }
   
  /**
   * Sets the weight of <code>this</code> edge 
   * @param weight the weight value of this edge
   */
   public void setWeight(int weight)  { this.weight = weight; }
  
  /**
   * Returns a string representation of <code>this</code> edge
   * @return type of edge followed by the source's name of this edge followed by the target's name of this edge
   */
   public String toString() 
   {
    return(type + " " + source.getName() + " " + target.getName());
   }
}
