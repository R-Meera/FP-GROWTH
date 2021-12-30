# FP-GROWTH

In this project we have implemented the FP-Growth Algorithm in the datasets that are available in UCI Repository.

Frequent Pattern Algorithm Steps:

1) Scan the database to find the occurrences of the itemsets in the database. This step is the same as the first
 step of Apriori
2) Construct the FP tree. For this, create the root of the tree. The root is represented by null.
3) Scan the database again and examine the transactions.
4) Scan the entire dataset and monitor all the transactions.
5) After examining or monitoring the first transaction find out the itemset in it
   scan the database to find the occurrences of the itemsets in the database. This step is the same as the first
 step of Apriori.
6) The itemset with the max count is taken at the top, the next itemset with lower count and so on
7) Also, the count of the itemset is incremented as it occurs in the transactions
8) The next step is to mine the created FP Tree.
9) For this, the lowest node is examined first along with the links of the lowest nodes. The lowest node represents the frequency pattern length 1.
10) Traverse the path in the FP Tree. This path or paths are called a conditional pattern base.
11) Conditional pattern base is a sub-database consisting of prefix paths in the FP tree occurring with the lowest node (suffix).
12) Construct a Conditional FP Tree, which is formed by a count of itemsets in the path. The itemsets meeting the threshold support are considered in the Conditional FP Tree.
13) Frequent Patterns are generated from the Conditional FP Tree.
