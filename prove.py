# Imports used for execution statistics & file parsing
import datetime as dt
import os 
import sys 

def main(args):
    time = dt.datetime.now();
    
    result = resolutionAlgorithm(args[0])
    print(result);
    runTime = dt.datetime.now() - time;
    
    if result != "":
        print("~~~~~~~~~~~~~~~~~~~~\nCompleted in: ", runTime);

def resolutionAlgorithm(inputFile):
    
    if (inputFile == "options"):
        printProofDirectory();
        return "";
    
    print("\n[Proving <"+inputFile+">]\n~~~~~~~~~~~~~~~~~~~~");
    
    # Get KB from file & Format it
    inputFile = "proofs/"+inputFile;
    kb = []
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
    i = 1;
    for cL1 in kb:
        j = 1;
        for cL2 in kb:
            result = checkResolvable(cL1, cL2,kb)
            if result == "FALSE":
                # FOUND CONTRADICTION
                print(str(line) + ". " + "Contradiction {"+str(i)+","+str(j)+"}")
                return "Valid";
            elif result != "" and result != None:
                # Add resolution to KB
                print(str(line) + ". ",clauseToString(result), " {"+str(i)+","+str(j)+"}")
                kb.append(result)
                line += 1
            j += 1; # Increment J
            if j >= i:
                break;
        i += 1; # Increment I
        
    return "Fail"

def formatLine(line):
    vars = []
    v = ""
    for c in line:
        if c != ' ' and c != '\n':
            v += c
        else:
            vars.append(v)
            v = ""
    if len(v) > 0:
        vars.append(v)
    map = {}
    for var in vars:
        if var.__contains__('~'):
            var = var.replace('~', '')
            map[var] = map.get(var, 0) - 1
        else:
            map[var] = map.get(var, 0) + 1
    return map;

def checkResolvable(cL1,cL2,kb):
    map = mergeClauses(cL1,cL2)
    if len(map) == 1:
        for k in map.keys():
            if map.get(k) == 0:
                return "FALSE"
    else:
        resolution = ""
        needRes = 0
        for var in map:
            if map.get(var) > 0: # pos
                if len(resolution) > 0:
                    resolution += " "
                resolution += var
            elif map.get(var) < 0: # neg
                if len(resolution) > 0:
                    resolution += " "
                resolution += ("~" + var)
            else:
                needRes += 1
        for x in map.values():
            if (x < -1) and (needRes != 1):
                return '';
            elif (x > 1) and (needRes != 1):
                return '';
        if needRes == 1:
            resolution = formatLine(resolution);
            if isDuplicate(resolution, kb) == False:
                return resolution
            else:
                return ""
        else:
            return ""

def negateClause(kb, clause):
    for v in clause:
        if clause[v] == -1:
            clause[v] = 1;
        else:
            clause[v] = -1;
    for newClause in clause:
        kb.append({newClause:clause.get(newClause)})
    return kb;

def isDuplicate(res, kb):
    for cL in kb:
        if res == cL:
            return True
    return False

def mergeClauses(cL1,cL2):
    map = {}
    for k in cL1.keys():
        map[k] = cL1[k];
    for k in cL2.keys():
        map[k] = map.get(k, 0) + cL2[k];
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
    
def printProofDirectory():
    print("\n[AVAILABLE PROOFS]");
    print("~~~~~~~~~~~~~~~~~~");
    for filename in os.listdir(os.getcwd()+"/proofs"):
        print(" ", filename);
    print("~~~~~~~~~~~~~~~~~~",end='');

if __name__ == '__main__':
    args = sys.argv[1:];
    if len(args) == 1:
        main(args);
