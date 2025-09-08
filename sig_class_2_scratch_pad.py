import itertools
from itertools import permutations, product
import copy
from collections import Counter

def createAdjList(sig: list[int]) -> list['Node']:
    adjList = []
    indexCounter = sum(sig) - 1 #indices = 0,1,...,numNodes -1
    for i in range(0, len(sig)):
        for j in range(0, sig[i]):
            adjList.append(Node(i+1, indexCounter)) #[2,1] -> [[1,[]],[1,[]],[2,[]]] adjList[x][0] = num cnctns, adjList[x][1] = indices cnctns
            indexCounter -= 1
    adjList.reverse() #reverse order for easier minNecStr construction
    return adjList
    
def edgeCalc(sig: list[int]) -> float:
    index = 1
    edgeCount = 0
    for i in sig:
        edgeCount += i * index
        index += 1
    return edgeCount/2
    
def connect(sig: 'Signature', i: 'Node', j: 'Node') -> 'Signature':
    sig.adjList[i.index].neighbors.append(j) #mutually add i and j to each other's cnctns indices
    sig.adjList[j.index].neighbors.append(i) #i and j = starting 0 enumerated labels for nodes 
    return sig

    
def genNbrCombinations(adjList: list['Node'], n: int) -> list[tuple['Node', ...]]:
    a = list(itertools.combinations(adjList, n))
    aSet = set(a)
    return list(aSet)
    
def genNbrCombinationsNode(adjList: list['Node'], node: 'Node') -> list[tuple['Node', ...]]:
    adjListCopy = copy.deepcopy(adjList)
    adjListCopy = [i for i in adjListCopy if i.index != node.index and len(i.neighbors) < i.degree]
    a = list(itertools.combinations(adjListCopy, node.numUnfilledNbrs()))
    aSet = set(a)
    return list(aSet)
    
def removeEdgeListCopies(edgeLists: list['EdgeList']) -> list['EdgeList']:
    remList = [False] * (len(edgeLists))
    for i in range(0, len(edgeLists) - 1):
        for j in range (i + 1, len(edgeLists)):
            if edgeLists[i].sameListDifferentOrderCheck(edgeLists[j]):
                remList[j] = True

    edgeLists = [edgeLists[i] for i in range(len(edgeLists)) if not remList[i]]
    
    return edgeLists
    
def groupedPermutations(groups: list[list['Node']]) -> list[list[int]]:
    #returns a list of lists of all permutations of node indices grouped by degree value
    # Generate permutations for each group
    groupPermutations = [list(permutations(group)) for group in groups]
    
    combinedResults = []
    for combination in product(*groupPermutations):
        # Flatten and concatenate the combination of tuples
        combinedList = [item for perm in combination for item in perm]
        combinedResults.append(combinedList)
    
    for i in combinedResults:
        print("combined results:", i)
    
    return combinedResults

def filterEdgeListByPermutation(edgeList: 'EdgeList', permutation: list[int]) -> 'EdgeList':
    # Create a mapping from original indices to permutation values
    indexMap = {i: permutation[i] for i in range(len(permutation))}
    
    # Apply the mapping to each edge
    transformedEdgeList = [[indexMap[u], indexMap[v]] for u, v in edgeList]
    
    #re-sort edges to be from lower index to higher (purely for ease of later comparison, no effect on results otherwise)
    for i in transformedEdgeList:
        if i[0] > i[1]:
            ph = i[0]
            i[0] = i[1]
            i[1] = ph
            
    return transformedEdgeList    
    
def addTail(signature: 'Signature', index: int) -> 'Signature':
    newSig = copy.deepcopy(signature.sig)
    newSig[0] += 1
    print("index = ", index, "len(newSig) = ", len(newSig))
    if index == len(newSig)-1:
        newSig.append(0)
    newSig[index] -= 1
    newSig[index+1] += 1
    print("newSig = ", newSig)
    return newSig
    
def connectDisconnected(signature: 'Signature', index1: int, index2: int) -> 'Signature':
    newSig = copy.deepcopy(signature.sig)
    print("newSig = ", newSig, "ind1 = ", index1, "ind2 = ", index2)
    if index1 == len(newSig) or index2 == len(newSig):
        newSig.append(0)
    print(newSig)
    newSig[index1-1] -= 1
    newSig[index1] += 1
    newSig[index2-1] -= 1
    newSig[index2] += 1
    return newSig
    
def genSigsAndConfigsUpToNNodes(maxNodes: int, seeds: list[list[int]], outputFilename: str) -> None:
    #seeds are just lists of ints representing the sig, not Signature objects
    for i in seeds:
        sig = Signature(i)
        sig.genAllConfigs()
        #gen and append tailSuccessors
        tailLeaves = sig.genSuccessorsFromTail()
        if sum(sig.sig) < maxNodes:
            for t in tailLeaves:
                if t not in seeds:
                    seeds.append(t)

        #gen and append CDCSuccessors
        CDCLeaves = sig.genSuccessorsCDC()
        for j in CDCLeaves:
            if j not in seeds:
                seeds.append(j)
        
        print("Remaining sigs to eval: ", len(seeds))
        f = open(outputFilename, 'a')
        f.write(str(i) + '\n')
        f.write("tailSuccessors:" + '\n')
        f.write(str(tailLeaves) + '\n')
        f.write("CDCSuccessors:" + '\n')
        f.write(str(CDCLeaves) + '\n')
        f.write("Configs:")
        for config in sig.configs:
            for edge in config.edgeList:
                f.write(str(edge))
            f.write('\n')
        f.write('\n')
        f.close()

def compareSignatures(sigOne, sigTwo):
    if sum(sigOne) > sum(sigTwo):
        return -1
    elif len(sigOne) < len(sigTwo):
        return 1
    elif len(sigTwo) > len(sigOne):
        return -1
    elif len(sigTwo) == len(sigOne) and sum(sigOne) == sum(sigTwo):
        for entry in range(0, len(sigTwo)):
            if sigOne[entry] > sigTwo[entry]:
                return 1
            elif sigOne[entry] < sigTwo[entry]:
                return -1
        
def orderSignatures(sigList):
    fullySorted = True
    for i in range(len(sigList) - 1):
        if compareSignatures(sigList[i], sigList[i+1]) == -1:
            a = sigList[i]
            sigList[i] = sigList[i+1]
            sigList[i+1] = a
            fullySorted = False
            
    if not fullySorted:
        sigList = orderSignatures(sigList)
    
    return sigList
        
    
class EdgeList:
    def __init__(self, edges: list[list[int]]) -> None:
        self.edgeList = edges
        
    def print(self):
        for i in self.edgeList:
            print(i)
        print()    
    
    def __hash__(self):
        return hash(tuple(self.edgeList))

    def sameListDifferentOrderCheck(self, other: 'EdgeList') -> bool:
    #since we are working with simple graphs, we only need to check for inclusion since all edges will be unique
        selfCopy = copy.deepcopy(self.edgeList)
        otherCopy = copy.deepcopy(other.edgeList)
        differences = [i for i in selfCopy if i not in otherCopy] #only checking for inclusion, not number of incidents, see above comment
                    
        if len(differences) == 0:
            return True
        else:
            return False
            
    def swapIndices(self, firstIndex: int, secondIndex: int) -> None:
        for i in self.edgList:
            if i[0] == firstIndex:
                i[0] = 'n'
            if i[1] == firstIndex:
                i[1] = 'n'
            if i[0] == secondIndex:
                i[0] = 'm'
            if i[1] == secondIndex:
                i[1] = 'm'

        for i in edgeListTwo:
            if i[0] == 'n':
                i[0] = secondIndex
            if i[1] == 'n':
                i[1] = secondIndex
            if i[0] == 'm':
                i[0] = firstIndex
            if i[1] == 'm':
                i[1] = firstIndex #swapPair indices in edgeListTwo now swapped

            
class Node:
    def __init__(self, degree: int, index: int) -> None:
        self.degree = degree
        self.neighbors = []
        self.index = index 
        
    def __eq__(self, other):
        return self.degree == other.degree and self.neighbors == other.neighbors
        
    def __hash__(self):
        return hash((self.degree, tuple(self.neighbors)))
            
    def print(self):
        print("index = ", self.index, "degree = ", self.degree, ":", self.nbrIndexList())
        
    def numUnfilledNbrs(self):
        return self.degree - len(self.neighbors)
        
    def nbrIndexList(self):
        l = []
        for i in self.neighbors:
            l.append(i.index)
        return l
        
class Signature:
    def __init__(self, sig: list[int]) -> 'Signature':
        self.sig = sig
        self.numEdges = edgeCalc(sig)
        self.numNodes = sum(sig)
        self.adjList = createAdjList(sig)
        self.configs = [] #expects edgelists of form (x, y) where x and y are specific indices of nodes to be cnctd
        
    def completionCheck(self):
        check = True
        for i in self.adjList:
            #print("CCeck: ind = ", i.index, " deg = ", i.degree, "nbrs = ", len(i.neighbors))
            if i.numUnfilledNbrs() != 0:
                check = False
        return check
    
    def potentialNeighbors(self, node: 'Node') -> list[int]: 
        #returns a list of indices of potentially neighboring nodes
        potentialNeighbors = copy.deepcopy(self.adjList)
        remList = [node.index]
        for i in potentialNeighbors:
            if(len(i.neighbors) == i.degree):
                remList.append(i.index)

        potentialNeighbors = [i for i in potentialNeighbors if i.index not in remList]

        return potentialNeighbors
        
    def currentGroupOpenEdges(self) -> int:
        currentGroup = []
        startNode = self.adjList[0]
        currentGroup.append(startNode)
        for i in startNode.neighbors:
            currentGroup.append(self.adjList[i.index])
            
        for i in currentGroup:
            for j in i.neighbors:
                included = False
                for k in currentGroup:
                    if k.index == j.index:
                        included = True
                if included == False:
                    currentGroup.append(self.adjList[j.index])
        openEdges = 0
        for i in currentGroup:
            openEdges += i.numUnfilledNbrs()

        return openEdges
    
    def disconnectedGroupCheck(self) -> bool: 
        workingGroupOpenEdges = self.currentGroupOpenEdges()
        totalOpenEdges = 0
        for i in self.adjList:
            totalOpenEdges += i.numUnfilledNbrs()

        if workingGroupOpenEdges == 0 and totalOpenEdges > 0:
            return True
        check = False

        for i in self.adjList:
            if len(self.potentialNeighbors(i)) < i.numUnfilledNbrs():
                check = True
        return check
            
    def debug(self):
        print(self.sig)
        print("num Edges = ", self.numEdges)
        print("num Nodes = ", self.numNodes)
        for i in self.adjList:
            i.print()
          
    def sortNodesByDegree(self: 'Signature') -> list[list['Node']]:
        #returns a list of all node groups (sorted by degree) with two or more members
        nodeGroups = []
        for i in range(len(self.sig) - 1, -1, -1):
            nodeGroups.append([])
            for j in self.adjList:
                if j.degree == i + 1:
                    nodeGroups[-1].append(j.index) 

        return nodeGroups
        
    def isomorphismTest(self, edgeListOne: 'EdgeList', edgeListTwo: 'EdgeList', swappablePairs: list[tuple['Node']]) -> bool:
        for swapPair in swappablePairs:
            firstIndex = swapPair[0].index
            secondIndex = swapPair[1].index
            
            edgeListTwo.swapIndices(firstIndex, secondIndex)

            if edgeListTwo.sameListDifferentOrderCheck(edgeListOne): #if the two lists are identical disregarding order
                return True
            edgeListTwo.swapIndices(firstIndex, secondIndex) #swap back for a clean slate for other checks

        return False #edgeListOne did not match any edgeListTwo after all applicable swaps
        
    def removeIsomorphicEdgeLists(self, masterEdgeLists: list['EdgeList']) -> list['EdgeList']:
        remList = [False] * (len(masterEdgeLists))
        nodeGroups = self.sortNodesByDegree()
        gp = groupedPermutations(nodeGroups)
        for i in range(len(masterEdgeLists)):
            filteredEdgeLists = []
            for perm in gp:
                filteredEdgeLists.append(filterEdgeListByPermutation(masterEdgeLists[i].edgeList, perm))
            for j in filteredEdgeLists:
                for k in range(i + 1, len(masterEdgeLists)): #added the +1 to the i so it doesn't compare a list to itself
                    if masterEdgeLists[k].sameListDifferentOrderCheck(EdgeList(j)):
                        remList[k] = True
                        
        finalEdgeLists = [masterEdgeLists[i] for i in range(len(masterEdgeLists)) if not remList[i]]

        return finalEdgeLists

    def genAllConfigs(self):
        workingSig = copy.deepcopy(self)
        workingList = copy.deepcopy(workingSig.adjList)
        completeCnxnLists = []

        retVals = self.iterate2(workingSig, [], [], 0, False)
        finalConfigSet = []
        for i in retVals[2]:
            finalConfigSet.append(EdgeList(i))
                    
        finalConfigSet = removeEdgeListCopies(finalConfigSet)
        
        if len(finalConfigSet) > 1:
            finalConfigSet = self.removeIsomorphicEdgeLists(finalConfigSet)
        for i in finalConfigSet:
            self.configs.append(i)
        print(self.sig, ": ", len(finalConfigSet)) 
 
    def identifyWorkingNode(self, workingSig: 'Signature') -> int:
        #returns the index of the first node in workingSig with fewer neighbors than its degree would imply
        workingNode = None
        for i in workingSig.adjList:
            if i.numUnfilledNbrs() > 0:
                workingNode = i
                return workingNode.index
     
    def iterate2(self, workingSig: 'Signature', cnxnList: list[tuple[int]], configList: list[list[tuple[int]]], level: int, debug: bool) ->None:
        level = level + 1
        if debug: print("Entered iterate2, level = ", level)
        if debug: print("configList = ")
        for i in configList:
            if debug: print(i)
        #depth first structure, paths are followed to the end until complete or disconnected, 
        #then the next branching paths one level higher are checked
        graphComplete = False #turns true if all nodes in graph are connected
        dcdGroup = False #turns true if a disconnected Group of nodes is formed
        finalPotentialNbrhd = False
        wn = None #wn = workingNode
        currentLevelConfigList = []
        crc = [] #current round connections, made on the present iteration
        wn = workingSig.adjList[self.identifyWorkingNode(workingSig)]
        nbrhdCombinations = genNbrCombinationsNode(workingSig.adjList, wn)

        for comb in nbrhdCombinations:
            if debug: print("wn = ")
            if debug: wn.print()
            if debug: print("testing combination:")
            for i in comb:
                if debug: i.print()
            if debug: print("current workingSig")
            for i in workingSig.adjList:
                if debug: i.print()
            if comb == nbrhdCombinations[-1]: finalPotentialNbrhd = True 
            for node in comb:
                connect(workingSig, wn, node) #connect working node with nodes in current potential nbrhd combination
                crc.append([wn.index, node.index]) #add most recently created edge to current round connections
            graphComplete = workingSig.completionCheck()
            if debug: print("graph full?:", graphComplete)
            if debug: print("pre DCGCheck:")
            if debug: workingSig.debug()
            dcdGroup = workingSig.disconnectedGroupCheck()
            if graphComplete:
                if finalPotentialNbrhd == True: #if graph is complete and all neighborhoods on this level have been checked
                    if debug: print("FPN = True")
                    currentLevelConfigList += [cnxnList + crc]
                    if debug:
                        for i in currentLevelConfigList:
                            print(i)
                    workingSig.deleteEdgeList(workingSig, crc) #remove current round connections from group
                    return[True, cnxnList + crc, currentLevelConfigList] #return true, current config, previous valid configs from this level
                else: #if current graph complete but there exist more potential neighborhoods on this level to check
                    currentLevelConfigList.append(list(cnxnList + crc)) #add config to final list of valid configs
                    if debug: print("in graph complete, nbrhds remaining, crc = ")
                    for i in crc:
                        if debug: print(i)
                    if debug: print("Current workingSig = ")
                    workingSig.debug()
                    workingSig.deleteEdgeList(workingSig, crc) #remove current round connections from group
                    if debug: print("post delete edgeList")
                    workingSig.debug()
            if dcdGroup: 
                if finalPotentialNbrhd == True: #if disconnectd group was formed and if last potential neighborhood to check
                    workingSig.deleteEdgeList(workingSig, crc) #TODO: testing this here, not sure if it works
                    return[False, [], configList] #return false and empty lists which we won't need
                else: #if disconnected group formed and more potential neighborhoods exist
                    workingSig.deleteEdgeList(workingSig, crc) #remove current round connections from group
                    crc = [] #reset currentRoundConnections after deleting from group
            if not graphComplete and not dcdGroup: #if current path is not invalid and graph incomplete
                retValues = workingSig.iterate2(workingSig, cnxnList + crc, configList + currentLevelConfigList, level, debug)
                if debug: print("Returned to level ", level)
                if debug: print("retValues = ", retValues)
                if debug: print("len retValues = ", len(retValues))
                for i in retValues:
                    if debug: print("RetValues = ", i)
                retGraphValid = retValues[0]
                retCnxnList = retValues[1]
                retConfigList = retValues[2]
                if retGraphValid == True:
                    configList.append(retCnxnList)
                configList = configList + retConfigList #this was the hangup to get all configs returned. Now there are duplicates of valid figs
                
                if finalPotentialNbrhd == False: #if there are more neighborhoods to check on this level
                    if debug: print("No more potenialNbrhds, crc = ")
                    for i in crc:
                        if debug: print(i)
                    if debug: print("cnxnList = ")
                    for i in cnxnList:
                        if debug: print(i)
                    if debug: print("retcnxnList = ")
                    for i in retCnxnList:
                        if debug: print(i)
                    if debug: print("configList = ")
                    for i in configList:
                        if debug: print(i)
                    workingSig.deleteEdgeList(workingSig, crc) #undo currentRoundConnections to test other potential nbrhds
                    crc = [] #reset CurrentRoundConnections to test other neighborhoods
                    if retGraphValid == True: 
                        configList = configList + retConfigList  #should probably be just cnfgLst = retConfgList
                elif finalPotentialNbrhd == True:#if there are no more potential neighborhoods on this level
                    configList = configList + retConfigList
                    workingSig.deleteEdgeList(workingSig, crc) #undo currentRoundConnections to test other potential nbrhds
            if debug: print("END of current NbrhdCombination")
        if debug: print("END of iterate2")
        return[False, cnxnList + crc, configList]
            
    def deleteEdgeList(self, workingSig: 'Signature', edgeList: 'EdgeList') -> None:
        #expects a list of tuples of indices of nodes to which the edge connects (e.g. [[0,1], [0,2]] deletes edges between 0 and 1 and 0 and 2
        for edge in edgeList:
            firstIndexNbrs = workingSig.adjList[edge[0]].neighbors
            for j in firstIndexNbrs:
                if j.index == edge[1]:
                    workingSig.adjList[edge[0]].neighbors.remove(j)
            secondIndexNbrs = workingSig.adjList[edge[1]].neighbors
            for j in secondIndexNbrs:
                if j.index == edge[0]:
                    workingSig.adjList[edge[1]].neighbors.remove(j)
                            
    def totalPotentialConnectablePairs(self):
        pot = []
        for i in range(0, len(self.sig)): #from index = 0 (deg 1 nodes) to index = numNodes-1
            if i == sum(self.sig) - 2:
            #we discard fully connected nodes which have an index val of numNodes - 1 (equals sum(self.sig) - 2)
                break
            if self.sig[i] > 0: #we discard index values with 0 nodes because no nodes of that connectivity exist to connect
                for j in range(0, self.sig[i]): #allows for same index connections such as (1,1), (2,2), etc.
                    pot.append(i + 1) # i + 1 because indices are zero indexed, the actual connectivity of those nodes is the index + 1
        firstPassCombinations = itertools.combinations(pot, 2) #2 because edges have two ends
        secondPassCombinations = set(firstPassCombinations)

        return secondPassCombinations
        
    def loadAdjFromConfig(self, edgeList: 'EdgeList') -> None:
    #assumes edgeList is a valid config
        self.adjList = createAdjList(self.sig) #clear current adjList
        for i in edgeList:
            connect(self, self.adjList[i[0]], self.adjList[i[1]])
        
    def findConnectablePairs(self):
        #TODO: add following heuristics: complete graphs -> no CP, 
        # [0...,n] nIndex < numNodes - 1 (i.e. incomplete graphs of single node degree) -> CP = nIndex, nIndex ([0,4] -> cp = (2,2)
        self.loadAdjFromConfig(self.configs[0].edgeList)
        potPairs = list(self.totalPotentialConnectablePairs())
        potPairBools = [[i, False] for i in potPairs]
        xNodes = []
        yNodes = []
        xyDisconnected = True
        for pair in potPairs:
            for config in self.configs:
                self.loadAdjFromConfig(config.edgeList)
                xNodes = [i for i in self.adjList if i.degree == pair[0]]
                yNodes = [i for i in self.adjList if i.degree == pair[1]]
                for xNode in xNodes:
                    for yNode in yNodes:
                        if xNode.index != yNode.index: #we skip evaluating instances where x and y are the same nodes
                            xyDisconnected = True #assume true and invalidate otherwise
                            for nbr in xNode.neighbors:
                                if nbr.index == yNode.index: #if one of x's neighbors shares y's index they they are connected
                                    xyDisconnected = False
                            if xyDisconnected == True:
                                for entry in potPairBools:
                                    if entry[0] == pair:
                                        entry[1] = True
                                break                   
                        if xyDisconnected == True:
                            break
                if xyDisconnected == True:
                    break
                else:
                    for entry in potPairBools:      #then nodes of deg x and deg y are implicitly connected
                        if entry[0] == pair:
                            entry[1] = entry[1] or False #accoutns for cases when final check returned false after earlier returned true
        connectablePairs = [potPairs[i] for i in range(len(potPairs)) if potPairBools[i][1] == True] #list comprehension to remove false potPairs 
        return connectablePairs
    
    def genSuccessorsFromTail(self):
        print("self.sig = ", self.sig)
        successors = []
        for i in range(0, len(self.sig)):
            if self.sig[i] > 0:
                print(i)
                print(self.sig[i])
                successors.append(addTail(self, i))
        return successors
        
    def genSuccessorsCDC(self):
        successors = []
        pairs = self.findConnectablePairs()
        for x, y in pairs:
            retSig = connectDisconnected(self, x, y)
            print("retSig = ", retSig)
            successors.append(retSig)
        return successors

testSigs = [[2],[2,1],[0,3],[2,2],[0,4],[1,2,1],[3,0,1],[0,2,2],[0,0,4],[2,3],[0,5],[3,1,1],[4,0,0,1],[2,1,2],[1,3,1],[2,2,0,1],[1,2,1,1],[0,4,0,1],[1,1,3],[0,3,2],[0,3,0,2],[1,0,3,1],[0,2,2,1],[0,1,4],[0,1,2,2],[0,0,4,1],[0,0,2,3],[0,0,0,5],[0,4,2],[0,0,6]]
#above are all sigs of graphlets from 2 to 5 nodes for testing purposes. All should return one config exept for [1,3,1] and [0,3,2]
testSigs4Nodes = [[2,2],[0,4],[1,2,1],[3,0,1],[0,2,2],[0,0,4]]
testSigs5Nodes = [[2,3],[0,5],[3,1,1],[4,0,0,1],[2,1,2],[1,3,1],[2,2,0,1],[1,2,1,1],[0,4,0,1],[1,1,3],[0,3,2],[0,3,0,2],[1,0,3,1],[0,2,2,1],[0,1,4],[0,1,2,2],[0,0,4,1],[0,0,2,3],[0,0,0,5]]

#generate all five node graphlets with sigs and conigs, write to "fiveNodeOutput.txt"
#only appends to output files, change name between runs to avoid duplicating the text
genSigsAndConfigsUpToNNodes(5, testSigs4Nodes, "fiveNodeOutputCleaned2.txt")
