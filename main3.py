#import datetime as dt
import sys

def main(args):
    #time = dt.datetime.now();
    print(resolutionAlgorithm(args[0]))
    #print(dt.datetime.now() - time)

def resolutionAlgorithm(inputFile):
    print(inputFile)
    kb = []
    # Get KB from file & Format it
    file = open(inputFile, 'r')
    for line in file:
        kb.append(formatLine(line))
    # Check KB and return if bad input
    if len(kb) == 0:
        return "File Format Incorrect";
    # Pop clause to test & Negate it
    kb = negateClause (kb, kb.pop())
    # Print what we've got so far
    line = 1;
    for cL in kb:
        s = clauseToString(cL)
        print(str(line) + ". " + s + " {}")
        line += 1
    # Loop through KB looking for resolutions
    i = 1; j = 0
    while i < len(kb):
        while j < i:
            result = resolveClauses(kb[i], kb[j])
            if result != None and len(result) == 0:    # if result is empty, we found contradiction
                print(str(line) + ". " + "Contradiction {"+str(i)+","+str(j)+"}")
                return "Valid"
            elif result != None and result not in kb:
                print(str(line) + ". ",clauseToString(result), " {"+str(i)+","+str(j)+"}")
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
    return map;

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

def negateClause(kb, clause):

    for v in clause:
        if clause[v] == -1:
            clause[v] = 1;
        else:
            clause[v] = -1;
    for newClause in clause:
        kb.append({newClause: clause.get(newClause)})
    return kb;

def isDuplicate(res, kb):
    for cL in kb:
        if res == cL:
            return True
    return False

def resolveClauses(cL1,cL2):
    hasPair = False
    map = {}
    for k in cL1.keys():
        map[k] = cL1[k];
    for k in cL2.keys():
        if k in map:
            # if k is negated in one clause but not in the other
            if (map[k] + cL2[k]) == 0:
                if (hasPair):   # if this is not the first complementary pair
                    return None
                else:           # if this is the first complementary pair
                    hasPair = True
                    del map[k]
        else:
            map[k] = cL2[k]
    return map

def clauseToString(cL):
    s = "";
    for c in cL:
        if len(s) != 0:
            s += " "
        if cL[c] == -1:
            s += "~"
        s += c
    return s;

if __name__ == '__main__':
    args = sys.argv[1:];
    if len(args) == 1:
        main(args);