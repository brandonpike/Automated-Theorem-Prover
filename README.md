# AI-KB_Resolution

# How to run the program
Commands: python main3.py <KB_File>

The KB file must contain the initial KB and the clause whose validity we want to test. The
input file contains n lines organized as follows: the first n − 1 lines describe the initial KB,
while line n contains the (original) clause to test. Note that the KB is written in CNF, so
each clause represents a disjunction of literals. The literals of each clause are separated by a
blank space, while negated variables are prefixed by ∼.

[~p q
~z y
~q p
q ~p z
q ~p ~z
~z y ~p]
