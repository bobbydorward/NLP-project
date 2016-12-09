/*
Parser.java
Parses a list of strings or list of tokens into its most probably parse tree using probabilistic
CKY.

Bobby Dorward
*/
import java.util.*;
import java.io.*;


public class Parser{
    
    String binaryFile = "binary.dat";
    String unaryFile = "unary.dat";
    String lexiconFile = "lexicon.dat";
    
    ArrayList<ArrayList<HashMap<Nonterminal,Tree>>> table;
    HashMap<Nonterminal,ArrayList<BinaryRule>> binaryMap;  //indexed by RHS0
    HashMap<Nonterminal,ArrayList<UnaryRule>> unaryMap;
    HashMap<String,ArrayList<LexRule>> lexMap;
    ArrayList<Nonterminal> nonterminals;
    public Parser(){
        binaryMap = new HashMap<Nonterminal,ArrayList<BinaryRule>>();
        unaryMap = new HashMap<Nonterminal,ArrayList<UnaryRule>>();
        lexMap = new HashMap<String,ArrayList<LexRule>>();
        nonterminals = new ArrayList<Nonterminal>();
        
        //read in binary file
        Scanner s = null;
        try {
             s= new Scanner(new File(binaryFile));
        } catch(FileNotFoundException e){
            System.err.println("file not found");
            System.exit(1);
        }
        while (s.hasNextLine()){
            String line = s.nextLine();
            Scanner lineScan = new Scanner(line);
            Nonterminal lhs = new Nonterminal(lineScan.next());
            if(!nonterminals.contains(lhs)){
                nonterminals.add(lhs);
            }
            lineScan.next();
            Nonterminal rhs0 = new Nonterminal(lineScan.next());
            if(!nonterminals.contains(rhs0)){
                nonterminals.add(rhs0);
            }
            Nonterminal rhs1 = new Nonterminal(lineScan.next());
            if(!nonterminals.contains(rhs1)){
                nonterminals.add(rhs1);
            }

            String probS = lineScan.next();
            Double prob = Double.parseDouble(probS.substring(1,probS.length()-1));
            BinaryRule bin = new BinaryRule(lhs,rhs0,rhs1,prob);
            if(!binaryMap.containsKey(rhs0)){
                ArrayList<BinaryRule> list = new ArrayList<BinaryRule>();
                list.add(bin);
                binaryMap.put(rhs0,list);
            } else {
                binaryMap.get(rhs0).add(bin);
            }
        }
        
        
        //read in unary file
        try {
             s= new Scanner(new File(unaryFile));
        } catch(FileNotFoundException e){
            System.err.println("file not found");
            System.exit(1);
        }
        while (s.hasNextLine()){
            String line = s.nextLine();
            Scanner lineScan = new Scanner(line);
            Nonterminal lhs = new Nonterminal(lineScan.next());
            if(!nonterminals.contains(lhs)){
                nonterminals.add(lhs);
            }
            lineScan.next();
            Nonterminal rhs0 = new Nonterminal(lineScan.next());
            if(!nonterminals.contains(rhs0)){
                nonterminals.add(rhs0);
            }
            String probS = lineScan.next();
            Double prob = Double.parseDouble(probS.substring(1,probS.length()-1));
            UnaryRule un = new UnaryRule(lhs,rhs0,prob);
            if(!unaryMap.containsKey(rhs0)){
                ArrayList<UnaryRule> list = new ArrayList<UnaryRule>();
                list.add(un);
                unaryMap.put(rhs0,list);
            } else {
                unaryMap.get(rhs0).add(un);
            }
        }
        
        //read in lexicon file
        try {
             s= new Scanner(new File(lexiconFile));
        } catch(FileNotFoundException e){
            System.err.println("file not found");
            System.exit(1);
        }
        while (s.hasNextLine()){
            String line = s.nextLine();
            Scanner lineScan = new Scanner(line);
            Nonterminal lhs = new Nonterminal(lineScan.next());
            if(!nonterminals.contains(lhs)){
                nonterminals.add(lhs);
            }
            lineScan.next();
            String rhs0 = lineScan.next();
            rhs0 = rhs0.substring(1,rhs0.length()-1);
            String probS = lineScan.next();
            Double prob = Double.parseDouble(probS.substring(1,probS.length()-1));
            LexRule l = new LexRule(lhs,rhs0,prob);
            if(!lexMap.containsKey(rhs0)){
                ArrayList<LexRule> list = new ArrayList<LexRule>();
                list.add(l);
                lexMap.put(rhs0,list);
            } else {
                lexMap.get(rhs0).add(l);
            }
        }
    }

    public void parseFile(String filename){
        Scanner s = null;
        try{
            s = new Scanner( new File(filename));
        } catch(FileNotFoundException e){
            System.err.println("no file");
            System.exit(1);
        }
        //input will be given as one sentence per line, white space delimited
        ArrayList<Tree> parsed_doc = new ArrayList<Tree>();
        while (s.hasNextLine()){
            String l = s.nextLine();
            Scanner s2 = new Scanner(l);
            ArrayList<TaggedWord> sentence = new ArrayList<TaggedWord>();
            while (s2.hasNext()){
                String word = s2.next();
                String tag = s2.next();
                sentence.add(new TaggedWord(word,tag));
            }
            if(sentence.size()==0){
                continue;
            }
            parsed_doc.add(parseTaggedWords(sentence));
        }
        PrintWriter writer=null;
        try{
            writer = new PrintWriter(filename+"_parsed", "UTF-8");
        } catch(FileNotFoundException e){
            System.err.println("no file");
            System.exit(1);
        } catch(UnsupportedEncodingException e){
            System.err.println("no file");
            System.exit(1);
        }
        for(Tree t : parsed_doc){
            writer.println(t.schemePrint());
        }
        writer.close();
    }
    
    public Tree parseStrings(List<String> sentence){
        //initialize table
        table = new ArrayList<ArrayList<HashMap<Nonterminal,Tree>>>();
        for(int i=0; i<sentence.size()+1;i++){
            ArrayList<HashMap<Nonterminal,Tree>> nextList = new ArrayList<HashMap<Nonterminal,Tree>>();
            table.add(nextList);
            for(int j=0; j<sentence.size()+1;j++){
                HashMap<Nonterminal,Tree> map = new HashMap<Nonterminal,Tree>();
                nextList.add(map);
            }
        }
        
        //perform probablistic CKY
        for(int j=1; j<=sentence.size();j++){
            String word = sentence.get(j-1);
            ArrayList<LexRule> lexRules = lexMap.get(word);
            //initialize base cases
            Tree wordTree = new Tree(word,1.0);
            HashMap<Nonterminal,Tree> curEntry = table.get(j-1).get(j);
            if(lexRules==null){
                return null;
            }
            for( LexRule r : lexRules){
                curEntry.put(r.lhs,new Tree(r.lhs.symbol,r.prob,wordTree));
            }
            
            //initialize unary of base cases
            boolean changes = true;
            while(changes){
                changes = false;
                Set<Nonterminal> keySet = new HashSet(curEntry.keySet());
                for(Nonterminal rhs : keySet){
                    ArrayList<UnaryRule> unList = unaryMap.get(rhs);
                    if(unList == null){
                        continue;
                    }
                    for(UnaryRule rule: unList){
                        Nonterminal lhs = rule.lhs;
                        Tree lhsTree = curEntry.get(lhs);
                        Tree rhsTree = curEntry.get(rhs);
                        Double rhsProb = rhsTree.probability;
                        Double newProb =rule.prob*rhsProb;
                        if((lhsTree==null)||(lhsTree.probability<newProb)){
                            curEntry.put(lhs,new Tree(lhs.symbol,newProb,rhsTree));
                            changes = true;
                        }
                    }
                }
                if(!changes){
                    break;
                }
            }
            for(int i = j-2; i>=0;i--){
                curEntry = table.get(i).get(j);
                for(int k = i+1; k<=j-1; k++){
                    for(Nonterminal nonterm : table.get(i).get(k).keySet()){
                        
                        //apply binary
                        ArrayList<BinaryRule> binList = binaryMap.get(nonterm);
                        if(binList == null){
                            continue;
                        }
                        for(BinaryRule rule : binList){
                            Nonterminal B = rule.rhs0;
                            Nonterminal C = rule.rhs1;
                            Nonterminal A = rule.lhs;
                            Tree Btree = table.get(i).get(k).get(B);
                            Double Bprob = Btree.probability;
                            Tree Ctree = table.get(k).get(j).get(C);
                            if(Ctree ==null){
                                continue;
                            }
                            Tree curTree = curEntry.get(A);
                            Double newProb = rule.prob*Bprob*Ctree.probability;
                            if(curTree == null || (curTree.probability<newProb)){
                                curEntry.put(A,new Tree(A.symbol,newProb,Btree,Ctree));
                            }
                        }
                    }
                }
                //apply unary
                changes = true;
                while(changes){
                    changes = false;
                    Set<Nonterminal> keySet = new HashSet(curEntry.keySet());
                    for(Nonterminal rhs : keySet){
                        ArrayList<UnaryRule> unList = unaryMap.get(rhs);
                        if(unList == null){
                            continue;
                        }
                        for(UnaryRule rule: unList){
                            Nonterminal lhs = rule.lhs;
                            Tree lhsTree = curEntry.get(lhs);
                            Tree rhsTree = curEntry.get(rhs);
                            Double rhsProb = rhsTree.probability;
                            Double newProb =rule.prob*rhsProb;
                            if((lhsTree==null)||(lhsTree.probability<newProb)){
                                curEntry.put(lhs,new Tree(lhs.symbol,newProb,rhsTree));
                                changes = true;
                        }
                    }
                    }
                    if(!changes){
                        break;
                    }
                }
            }
            
            
            
        }
        //System.out.println(table.get(0).get(sentence.size()));
        Tree finalTree = table.get(0).get(sentence.size()).get(new Nonterminal("S"));
        return finalTree;
    }
    
    public Tree parseTaggedWords(List<TaggedWord> sentence){
        //initialize table
        table = new ArrayList<ArrayList<HashMap<Nonterminal,Tree>>>();
        for(int i=0; i<sentence.size()+1;i++){
            ArrayList<HashMap<Nonterminal,Tree>> nextList = new ArrayList<HashMap<Nonterminal,Tree>>();
            table.add(nextList);
            for(int j=0; j<sentence.size()+1;j++){
                HashMap<Nonterminal,Tree> map = new HashMap<Nonterminal,Tree>();
                nextList.add(map);
            }
        }
        
        //perform probablistic CKY
        for(int j=1; j<=sentence.size();j++){
            TaggedWord taggedword = sentence.get(j-1);
            //initialize base cases
            Tree wordTree = new Tree(taggedword.getTag(),1.0,new Tree(taggedword.getWord(),1.0));
            HashMap<Nonterminal,Tree> curEntry = table.get(j-1).get(j);
            curEntry.put(new Nonterminal(taggedword.getTag()),wordTree);
        
            
            //initialize unary of base cases
            boolean changes = true;
            while(changes){
                changes = false;
                Set<Nonterminal> keySet = new HashSet(curEntry.keySet());
                for(Nonterminal rhs : keySet){
                    ArrayList<UnaryRule> unList = unaryMap.get(rhs);
                    if(unList == null){
                        continue;
                    }
                    for(UnaryRule rule: unList){
                        Nonterminal lhs = rule.lhs;
                        Tree lhsTree = curEntry.get(lhs);
                        Tree rhsTree = curEntry.get(rhs);
                        Double rhsProb = rhsTree.probability;
                        Double newProb =rule.prob*rhsProb;
                        if((lhsTree==null)||(lhsTree.probability<newProb)){
                            curEntry.put(lhs,new Tree(lhs.symbol,newProb,rhsTree));
                            changes = true;
                        }
                    }
                }
                if(!changes){
                    break;
                }
            }
            for(int i = j-2; i>=0;i--){
                curEntry = table.get(i).get(j);
                for(int k = i+1; k<=j-1; k++){
                    for(Nonterminal nonterm : table.get(i).get(k).keySet()){
                        
                        //apply binary
                        ArrayList<BinaryRule> binList = binaryMap.get(nonterm);
                        if(binList == null){
                            continue;
                        }
                        for(BinaryRule rule : binList){
                            Nonterminal B = rule.rhs0;
                            Nonterminal C = rule.rhs1;
                            Nonterminal A = rule.lhs;
                            Tree Btree = table.get(i).get(k).get(B);
                            Double Bprob = Btree.probability;
                            Tree Ctree = table.get(k).get(j).get(C);
                            if(Ctree ==null){
                                continue;
                            }
                            Tree curTree = curEntry.get(A);
                            Double newProb = rule.prob*Bprob*Ctree.probability;
                            if(curTree == null || (curTree.probability<newProb)){
                                curEntry.put(A,new Tree(A.symbol,newProb,Btree,Ctree));
                            }
                        }
                    }
                }
                //apply unary
                changes = true;
                while(changes){
                    changes = false;
                    Set<Nonterminal> keySet = new HashSet(curEntry.keySet());
                    for(Nonterminal rhs : keySet){
                        ArrayList<UnaryRule> unList = unaryMap.get(rhs);
                        if(unList == null){
                            continue;
                        }
                        for(UnaryRule rule: unList){
                            Nonterminal lhs = rule.lhs;
                            Tree lhsTree = curEntry.get(lhs);
                            Tree rhsTree = curEntry.get(rhs);
                            Double rhsProb = rhsTree.probability;
                            Double newProb =rule.prob*rhsProb;
                            if((lhsTree==null)||(lhsTree.probability<newProb)){
                                curEntry.put(lhs,new Tree(lhs.symbol,newProb,rhsTree));
                                changes = true;
                        }
                    }
                    }
                    if(!changes){
                        break;
                    }
                }
            }
            
            
            
        }
        //System.out.println(table.get(0).get(sentence.size()));
        Tree finalTree = table.get(0).get(sentence.size()).get(new Nonterminal("S"));
        return finalTree;
    }
    
    
    //public static void main(String[] args){
    //    Parser p = new Parser();
    //    ArrayList<String> test = new ArrayList<String>();
    //    test.add("can");
    //    test.add("I");
    //    test.add("seasonally");
    //    test.add("fly");
    //    test.add("the");
    //    test.add("flights");
    //    test.add("and");
    //    test.add("slide");
    //    test.add("an");
    //    test.add("atmosphere");
    //    
    //    ArrayList<TaggedWord> tag = new ArrayList<TaggedWord>();
    //    tag.add(new TaggedWord("can","S"));
    //    tag.add(new TaggedWord("I","S"));
    //    System.out.println(p.parseStrings(test));
    //    System.out.println(p.parseTaggedWords(tag));
    //}
    
    
    
    private class Entry{
        Tree tree;
        Double prob;
        public Entry(Tree t, Double prob){
            this.tree= t;
            this.prob = prob;
        }
    }

    public static void main(String[] args){
        String filename = args[0];
        Parser p = new Parser();
        p.parseFile(filename);
    }
}