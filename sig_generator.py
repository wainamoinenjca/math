import copy

def edgeCalc(sig):
    index = 1
    edgeCount = 0
    for i in sig:
        edgeCount += i * index
        index += 1
    return edgeCount/2

def genConnectablePairs(sig):
    n = sum(sig) #number of nodes in sig
    #print(n)
    #print(sig[len(sig) - 1])
    indexVals = [] #holds index values of potentially connectable nodes
    connectablePairs = [] #holds pairs of potentially connectable node indices (e.g. [0,3,2]->[2, 2], [2,3], [3,3])
    for i in range(0, min(n-2, len(sig))): #min accts for sigs w/o fully connected nodes
        if sig[i] > 0:
            indexVals.append([sig[i], i + 1]) #i nodes of index j ([0,3,2] -> [3, 2][2, 3]
                                              #adding 1 to get 0 starting enumeration to match index value
    for i in indexVals:
        print(i, " = indexVal")
    for i in range(0, len(indexVals)):                       
        if indexVals[i][0] > 1: #if there is more than one node of a given index value
            connectablePairs.append([indexVals[i][1], indexVals[i][1]]) #add pair of index value of i
            for j in range(i + 1, len(indexVals)): #+1 to avoid double counting same index pairs ([2, 2], [3, 3]
                connectablePairs.append([indexVals[i][1], indexVals[j][1]]) #add pair of index values of i and j
    
    for i in connectablePairs:
        print(i, " = connectablePair")
    
    return connectablePairs
    
def connectDisconnected(sig):
    connectablePairs = genConnectablePairs(sig)
    for i in connectablePairs:
        newSig = copy.deepcopy(sig)
        while (len(newSig) < sum(newSig) - 1): #add trailing zeroes up to max connected index(=n-1)
            newSig = newSig + [0]
        print(newSig, " = copySig")
        print(i, " = i")
        for j in i:
            print(j, " = j")
            newSig[j - 1] = newSig[j - 1] - 1
            newSig[j] = newSig[j] + 1
        print(newSig, " = newSig")
    

    return

def addTail(sig):
    numNodes = lambda sig: sum(sig)
    numEdges = edgeCalc(sig)
    print("numNodes = ", numNodes(sig))
    print("numEdges = ", numEdges)
    newSigs = []
    index = 1
    for n in sig:
        print('n = ', n)
        if n != 0: #if n == 0 then there are no deg=index nodes to add a tail to
            newSig = copy.deepcopy(sig)
            print("1", newSig, sig)
            if index == len(sig):
                newSig = sig + [0]
                sig = sig + [0]
            newSig[index-1] = sig[index-1] - 1 #subtract one deg = index node
            print("2", newSig, sig)
            newSig[index] = sig[index] + 1 #add one deg = index+1 node
            print("3", newSig, sig)
            newSig[0] = newSig[0] + 1 #add deg 1 node to deg 1 column (0 since python starts counting from 0)
            print("4", newSig, sig)
            index += 1
            newSigs.append(copy.deepcopy(newSig))
        else:
            index += 1
            continue
    for ns in newSigs: print(ns)
    
#addTail([0,3,2])
#genConnectablePairs([0,3,2])
connectDisconnected([4,0,0,1])
print()
connectDisconnected([0,3,2])
print()
connectDisconnected([0,3,0,2])
