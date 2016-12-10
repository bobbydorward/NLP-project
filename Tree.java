public class Tree {
  private String symbol;
  private boolean isLeaf;
  public double probability;
  private int nchildren;
  private Tree lchild;
  private Tree rchild;
  
  public Tree(String symbol,double probability,Tree lchild,Tree rchild){
    this.symbol = symbol;
    this.isLeaf = false;
    this.probability = probability;
    this.nchildren = 2;
    this.lchild = lchild;
    this.rchild = rchild;
  }
  
  public Tree(String symbol,double probability,Tree child){
    this(symbol,probability,child,null);
    this.nchildren = 1;
  }

  public Tree(String symbol,double probability){
    this(symbol,probability,null,null);
    this.isLeaf = true;
    this.nchildren = 0;
  }

  public String schemePrint(){
    return schemePrintHelper();
  }

  public String schemePrintHelper(){
    if(isLeaf){
      return this.symbol;
    }
    if(nchildren ==1){
      return "("+this.symbol+" "+lchild.schemePrintHelper()+")";
    }
    return "("+this.symbol +" "+ lchild.schemePrintHelper() +" "+ rchild.schemePrintHelper()+")";
  }
  
  private String toString(String pre){
    String s=pre;
    if(isLeaf)
      s += symbol.toString();
    else if(nchildren == 1){
      s += "(" + symbol + " [" + probability + "]\n";
      s += lchild.toString(pre+"   ");
      s += "\n"+pre+")";
    }
    else if(symbol.toString().indexOf('|')>=0){ 
      s = lchild.toString(pre);
      s += "\n";
      s += rchild.toString(pre);
    }
    else {
      s += "(" + symbol + " [" + probability + "]\n";
      s += lchild.toString(pre+"   ");
      s += "\n";
      s += rchild.toString(pre+"   ");
      s += "\n"+pre+")";
    }
    return s;
  }    
  
  public String toString(){
    return toString("");
  }
  
}
