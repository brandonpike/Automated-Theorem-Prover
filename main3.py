#import datetime as dt
import sys

# def resolveClauses(cL1, cL2):
#     hasPair = False
#     map = {}
#     for k in cL1.keys():
#         map[k] = cL1[k]
#     for k in cL2.keys():
#         if k in map:
#             # if k is negated in one clause but not in the other
#             if (map[k] + cL2[k]) == 0:
#                 if hasPair:   # if this is not the first complementary pair
#                     return None
#                 else:           # if this is the first complementary pair
#                     hasPair = True
#                     del map[k]
#         else:
#             map[k] = cL2[k]
#     if hasPair:
#         return map
#     else:
#         return None


class KbClause:
    """
    Represents a clause in the knowledge base.
    """

    def __init__(self, atoms, negAtoms, parents=()):
        self.atoms = frozenset(atoms)
        self.negAtoms = frozenset(negAtoms)
        self.atomOrder = tuple(atoms)
        self.parents = parents

    def __eq__(self, other):
        return self.atoms == other.atoms and self.negAtoms == other.negAtoms

    def __hash__(self):
        return hash((self.atoms, self.negAtoms))

    def negate(self):
        result = []
        for atom in self.atomOrder:
            if atom in self.negAtoms:
                result.append(KbClause((atom), ()))
            else:
                result.append(KbClause((atom), (atom)))
        return result

    def resolve(self, other):
        # eliminate duplicate literals
        intersect = self.literals.union(other.literals)

    def toString(self):
        string = ""
        for atom in self.atomOrder:
            if atom in self.negAtoms:
                string += "~"
            string += atom
            string += " "
        return string

class KnowledgeBase:
    """
    Represents the knowledge base.
    """

    def __init__(self):
        self.clauses = set()
        self.clauseOrder = []

    def addClause(self, clause):
        # don't add logical duplicates of existing clauses
        if clause not in self.clauses:
            self.clauses.add(clause)
            self.clauseOrder.append(clause)

    def pop(self):
        clause = self.clauseOrder.pop()
        self.clauses.discard(clause)
        return clause

    def getClause(self, index):
        return clauseOrder[index]


def initializeKb(inputFile):
    kb = KnowledgeBase()

    file = open(inputFile, 'r')
    for line in file:
        atoms, negAtoms = extractAtoms(line)
        kb.addClause(KbClause(atoms, negAtoms))
    # remove clause to be negated
    testClauses = kb.pop().negate()
    # add negated clause(s) to kb
    for clause in testClauses:
        kb.addClause(clause)
    return kb


def main(args):
    #time = dt.datetime.now();
    kb = initializeKb(args[0])

    # Print what we've got so far
    line = 1
    for cL in kb.clauseOrder:
        s = cL.toString()
        print(str(line) + ". " + s + "{}")
        line += 1

    # resolutionAlgorithm(kb)
    #print(dt.datetime.now() - time)


def resolutionAlgorithm(kb):

    # Loop through KB looking for resolutions
    i = 1
    while i < len(kb.clauses):
        j = 0
        while j < i:
            result = resolveClauses(kb[i], kb[j])
            # if result is empty, we found contradiction
            if result != None and len(result) == 0:
                print(str(line) + ". " +
                      "Contradiction {"+str(i + 1)+","+str(j + 1)+"}")
                return "Valid"
            elif result != None and result not in kb:
                print(str(line) + ". ", clauseToString(result),
                      " {"+str(i + 1)+","+str(j + 1)+"}")
                kb.append(result)
                line += 1
            j += 1
        i += 1
    return "Fail"

    # i = 1;
    # for cL1 in kb:
    #     j = 1;
    #     for cL2 in kb:
    #         result = checkResolvable(cL1, cL2,kb)
    #         if result == "FALSE":
    #             # FOUND CONTRADICTION
    #             print(str(line) + ". " + "Contradiction {"+str(i)+","+str(j)+"}")
    #             return "Valid";
    #         elif result != "" and result != None:
    #             # Add resolution to KB
    #             print(str(line) + ". ",clauseToString(result), " {"+str(i)+","+str(j)+"}")
    #             kb.append(result)
    #             line += 1
    #         j += 1; # Increment J
    #         if j >= i:
    #             break;
    #     i += 1; # Increment I
    # return "Fail"


def formatLine(line):
    vars = line.split()
    map = {}
    for var in vars:
        if var.startswith('~'):
            var = var.lstrip('~')
            map[var] = -1
        else:
            map[var] = 1
    return map


def extractAtoms(clause):
    literals = clause.split()
    atoms = []
    negAtoms = []

    for lit in literals:
        isNegated = False
        # check for negation and remove '~' character
        if lit.startswith('~'):
            isNegated = True
            lit = lit.lstrip('~')
        # don't add duplicate atoms
        if lit not in atoms:
            atoms.append(lit)
            if isNegated:
                negAtoms.append(lit)
        # # # if the non-negated atom already exists
        # elif isNegated and lit not in negAtoms:
        #     return True     # clause evaluates to true

    return (atoms, negAtoms)


# def checkResolvable(cL1,cL2,kb):
#     map = mergeClauses(cL1,cL2)
#     if len(map) == 1:
#         for k in map.keys():
#             if map.get(k) == 0:
#                 return "FALSE"
#     else:
#         resolution = ""
#         needRes = 0
#         for var in map:
#             if map.get(var) > 0: # pos
#                 if len(resolution) > 0:
#                     resolution += " "
#                 resolution += var
#             elif map.get(var) < 0: # neg
#                 if len(resolution) > 0:
#                     resolution += " "
#                 resolution += ("~" + var)
#             else:
#                 needRes += 1
#         for x in map.values():
#             if (x < -1) and (needRes != 1):
#                 return '';
#             elif (x > 1) and (needRes != 1):
#                 return '';
#         if needRes == 1:
#             resolution = formatLine(resolution);
#             if isDuplicate(resolution, kb) == False:
#                 return resolution
#             else:
#                 return ""
#         else:
#             return ""

def negateClause(clause):
    result = []
    for key in clause:
        val = clause[key] * -1
        result.append({key: val})
    return result


def negateClause(kb, clause):

    for v in clause:
        if clause[v] == -1:
            clause[v] = 1
        else:
            clause[v] = -1
    for newClause in clause:
        kb.append({newClause: clause.get(newClause)})
    return kb


def isDuplicate(res, kb):
    for cL in kb:
        if res == cL:
            return True
    return False

# def resolveClauses(cL1, cL2):
#     hasPair = False
#     map = {}
#     for k in cL1.keys():
#         map[k] = cL1[k]
#     for k in cL2.keys():
#         if k in map:
#             # if k is negated in one clause but not in the other
#             if (map[k] + cL2[k]) == 0:
#                 if hasPair:   # if this is not the first complementary pair
#                     return None
#                 else:           # if this is the first complementary pair
#                     hasPair = True
#                     del map[k]
#         else:
#             map[k] = cL2[k]
#     if hasPair:
#         return map
#     else:
#         return None


def clauseToString(cL):
    s = ""
    for c in cL:
        if len(s) != 0:
            s += " "
        if cL[c] == -1:
            s += "~"
        s += c
    return s


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) == 1:
        main(args)
