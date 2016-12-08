public class LexRule extends PCFGRule {
  private String rhs;

  public LexRule(Nonterminal lhs,String rhs,double prob){
    super(lhs,prob);
    this.rhs = rhs;
  } 
  
  public String toString(){
    return lhs+" ==> '"+rhs+"' ["+prob+"]";
  }
}
