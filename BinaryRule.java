class BinaryRule extends PCFGRule {
  Nonterminal rhs0;
  Nonterminal rhs1;
  
  BinaryRule(Nonterminal lhs,Nonterminal rhs0,Nonterminal rhs1,double prob){
    super(lhs,prob);
    this.rhs0 = rhs0;
    this.rhs1 = rhs1;
  }
  
  public String toString(){
    return lhs+" ==> "+rhs0+" "+rhs1+" ["+prob+"]";
  }  
}
