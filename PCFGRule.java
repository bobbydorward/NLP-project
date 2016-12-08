public class PCFGRule {
  protected Nonterminal lhs;
  protected double prob;

  public PCFGRule(Nonterminal lhs,double prob){
    this.lhs = lhs;
    this.prob = prob;
  }    
}
