public class UnaryRule extends PCFGRule {
  private Nonterminal rhs;

  public UnaryRule(Nonterminal lhs,Nonterminal rhs,double prob){
    super(lhs,prob);
    this.rhs = rhs;
  }
  
  public String toString(){
    return lhs+" ==> "+rhs+" ["+prob+"]";
  }  
}
