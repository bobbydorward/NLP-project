public class Nonterminal {
  public String symbol;
  
  public Nonterminal(String symbol){
    this.symbol = symbol;
  }
  
  public String toString(){
    return symbol;
  }
  @SuppressWarnings("unchecked")
  @Override
  public boolean equals(Object o){
      if(this== o){
          return true;
      }
      if(o==null){
          return false;
      }
      if(this.getClass() !=o.getClass()){
          return false;
      }
      Nonterminal a = (Nonterminal) o;
      if(this.symbol.equals(a.symbol)){
        return true;
      }
      return false;
  }
  public int hashCode(){
    return this.symbol.hashCode();
  }
  
}
