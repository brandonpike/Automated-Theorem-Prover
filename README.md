# Automated Theorem Prover

# The point of the program
a) Demonstrating theorem proving with <b>no libraries imported</b><br/>
b) This program takes a knowledge base represented in CNF and tries to prove a clause by contradiction. 
We demonstrate the resolution principle listed at the bottom of this document.

# How to run the program
Commands: 
python prove.py options (gives you available proofs)<br/>
python prove.py <filename.in> (prove theorem)

The KB file must contain the initial KB and the clause whose validity we want to test. The
input file contains n lines organized as follows: the first n − 1 lines describe the initial KB,
while line n contains the (original) clause to test. Note that the KB is written in CNF, so
each clause represents a disjunction of literals. The literals of each clause are separated by a
blank space, while negated variables are prefixed by ∼.

Example Input File: test.kb

∼p q<br/>
∼z y<br/>
p<br/>
∼z y<br/>

Example Output:
1. ∼p q {}
2. ∼z y {}
3. p {}
4. z {}
5. ∼y {}
6. q {3, 1}
7. y {4, 2}
8. ∼z {5, 2}
6. Contradiction {7, 5}<br/>
Valid

# The Resolution Principle
  To prove that a clause is valid using the resolution method, we attempt to show that the negation
  of the clause is unsatisfiable, meaning it cannot be true under any truth assignment. This is done
  using the following algorithm:
  1. Negate the clause and add each literal in the resulting conjunction of literals to the set of
  clauses already known to be valid.
  2. Find two clauses for which the resolution rule can be applied. Change the form of the
  produced clause to the standard form and add it to the set of valid clauses.
  3. Repeat 2 until False is produced, or until no new clauses can be produced. If no new clauses
  can be produced, report failure; the original clause is not valid. If False is produced, report
  success; the original clause is valid.
