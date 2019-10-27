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
    def __init__(self, atoms, negAtoms, clauseNumber, parents=()):
        self.atoms = frozenset(atoms)
        self.negAtoms = frozenset(negAtoms)
        self.atomOrder = tuple(atoms)
        self.clauseNumber = clauseNumber
        self.parents = tuple(parents)

    def __eq__(self, other):
        return self.atoms == other.atoms and self.negAtoms == other.negAtoms

    def __hash__(self):
        return hash((self.atoms, self.negAtoms))

    def negate(self):
        result = []
        clauseNum = self.clauseNumber
        for atom in self.atomOrder:
            if atom in self.negAtoms:
                result.append(KbClause((atom), (), clauseNum))
            else:
                result.append(KbClause((atom), (atom), clauseNum))
            clauseNum += 1
        return result

    def resolve(self, other, clauseNumber):
        nonNegAtoms1 = self.atoms.difference(self.negAtoms)
        nonNegAtoms2 = other.atoms.difference(other.negAtoms)

        # find atoms in complementary literals
        intersect1 = nonNegAtoms1.intersection(other.negAtoms)
        intersect2 = nonNegAtoms2.intersection(self.negAtoms)
        complementAtoms = intersect1.union(intersect2)

        # if there is not exactly 1 pair of complementary literals,
        # do not resolve
        if len(complementAtoms) != 1:
            return None

        # atoms in the resulting clause
        atomUnion = self.atoms.union(other.atoms).difference(complementAtoms)
        # order the atoms based on previous atom order
        resultAtoms = []
        for a in self.atomOrder:
            if a in atomUnion:
                resultAtoms.append(a)
        for a in other.atomOrder:
            if a in atomUnion and a not in resultAtoms:
                resultAtoms.append(a)

        # negated atoms in the resulting clause
        negAtomUnion = self.negAtoms.union(other.negAtoms).difference(complementAtoms)

        # return resulting clause
        return KbClause(resultAtoms, negAtomUnion, clauseNumber, (self.clauseNumber, other.clauseNumber))


    def toString(self):
        string = f'{self.clauseNumber}. '
        for atom in self.atomOrder:
            if atom in self.negAtoms:
                string += "~"
            string += atom
            string += " "
        if self.parents:
            string += "{{{0}, {1}}}".format(*self.parents)
        else:
            string += "{}"
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
    lineNumber = 1
    for line in file:
        atoms, negAtoms = extractAtoms(line)
        kb.addClause(KbClause(atoms, negAtoms, lineNumber))
        lineNumber += 1

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
    for clause in kb.clauseOrder:
        print(clause.toString())

    resolutionAlgorithm(kb)
    #print(dt.datetime.now() - time)


def resolutionAlgorithm(kb):

    # Loop through KB looking for resolutions
    line = len(kb.clauses) + 1
    i = 1
    while i < len(kb.clauses):
        j = 0
        while j < i:
            result = kb.clauseOrder[i].resolve(kb.clauseOrder[j], line)
            # if result is empty, we found contradiction
            if result is not None and len(result.atoms) == 0:
                print(str(line) + ". Contradiction {"+str(i + 1)+", "+str(j + 1)+"}")
                print("Valid")
                return 0
            elif result is not None and result not in kb.clauses:
                print(result.toString())
                kb.addClause(result)
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
