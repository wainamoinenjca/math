import itertools
from itertools import permutations, product
import copy
from collections import Counter

def createAdjList(sig):
    adjList = []
    indexCounter = sum(sig) - 1 #indices = 0,1,...,numNodes -1
    for i in range(0, len(sig)):
        for j in range(0, sig[i]):
            adjList.append(Node(i+1, indexCounter)) #[2,1] -> [[1,[]],[1,[]],[2,[]]] adjList[x][0] = num cnctns, adjList[x][1] = indices cnctns
            indexCounter -= 1
    adjList.reverse() #reverse order for easier minNecStr construction
    #print(adjList)
    return adjList
    
def edgeCalc(sig):
    index = 1
    edgeCount = 0
    for i in sig:
        edgeCount += i * index
        index += 1
    return edgeCount/2
    
def connect(sig, i, j):
    #add check to ensure both are not fully connected
    #print("in connect: sig.adjList = ")
    #for n in sig.adjList:
    #    n.print()
    #iInd = sig.adjList[i].index
    #jInd = sig.adjList[j].index
    #print("connecting nodes ", i.index, " and ", j.index)
    sig.adjList[i.index].neighbors.append(j) #mutually add i and j to each other's cnctns indices
    sig.adjList[j.index].neighbors.append(i) #i and j = starting 0 enumerated labels for nodes 
    return sig

    
def genNbrCombinations(adjList, n):
    #for a in adjList:
    #    a.print()
    #connect(adjList, 0, 1)
    
    a = list(itertools.combinations(adjList, n))
 #   for i in a:
 #       for j in i:
#            j.print()
#        print()
    aSet = set(a)
 #   print("final set")
#    for a in aSet:
#        for b in a:
#            b.print()
#        print()
    return list(aSet)
    
def genNbrCombinationsNode(adjList, node):
    adjListCopy = copy.deepcopy(adjList)
    #for i in adjListCopy:
    #    if i.index == node.index:
    #        adjListCopy.remove(i)
    adjListCopy = [i for i in adjListCopy if i.index != node.index and len(i.neighbors) < i.degree]
    a = list(itertools.combinations(adjListCopy, node.numUnfilledNbrs()))
    aSet = set(a)
    return list(aSet)
    
def removeEdgeListCopies(edgeLists):
    #print("len edgeLists = ", len(edgeLists))
    #print("in RELC:, pre processing = ")
    #for i in edgeLists:
    #    i.print()
    remList = [False] * (len(edgeLists))
    for i in range(0, len(edgeLists) - 1):
        for j in range (i + 1, len(edgeLists)):
            if edgeLists[i].sameListDifferentOrderCheck(edgeLists[j]):
                #print(i, j, "match")
                remList[j] = True
    #for i in range(len(remList)):
    #    print(i, remList[i])

    #[main_list[i] for i in range(len(bool_list)) if not bool_list[i]]
    edgeLists = [edgeLists[i] for i in range(len(edgeLists)) if not remList[i]]
    #print("in RELC:, final list = ")
    #for i in edgeLists:
    #    i.print()
    
    return edgeLists
    
def genSwappablePairs(groupList): #depreciated, remove
    pairCombinationsByDegree = []
    for i in groupList:
        swapPairs = itertools.combinations(i, 2)
        pairCombinationsByDegree.append(swapPairs)

    #for i in pairCombinationsByDegree:
        #for j in i:
            #for k in j:
                #k.print()
            #print()
            
    return pairCombinationsByDegree
    
def groupedPermutations(groups):
    # Generate permutations for each group
    groupPermutations = [list(permutations(group)) for group in groups]
    
    # Combine permutations from different groups
    combinedResults = []
    for combination in product(*groupPermutations):
        # Flatten and concatenate the combination of tuples
        combinedList = [item for perm in combination for item in perm]
        combinedResults.append(combinedList)
    
    return combinedResults

def filterEdgeListByPermutation(edgeList, permutation):
    # Create a mapping from original indices to permutation values
    indexMap = {i: permutation[i] for i in range(len(permutation))}
    
    # Apply the mapping to each edge
    transformedEdgeList = [[indexMap[u], indexMap[v]] for u, v in edgeList]
    
    #resort edges to be from lower index to higher (purely for ease of later comparison, no effect on results otherwise)
    for i in transformedEdgeList:
        if i[0] > i[1]:
            ph = i[0]
            i[0] = i[1]
            i[1] = ph
            
    return transformedEdgeList    
    
class EdgeList:
    def __init__(self, edges):
        self.edgeList = edges
        
    def print(self):
        for i in self.edgeList:
            print(i)
        print()    
    
    def __hash__(self):
        return hash(tuple(self.edgeList))

    def sameListDifferentOrderCheck(self, other):
    #since we are working with simple graphs, we only need to check for inclusion since all edges will be unique
        selfCopy = copy.deepcopy(self.edgeList)
        otherCopy = copy.deepcopy(other.edgeList)
        differences = [i for i in selfCopy if i not in otherCopy] #only checking for inclusion, not number of incidents, see above comment
        #for i in differences:
        #    print("diffs: ", i)
                    
        if len(differences) == 0:
            return True
        else:
            return False
            
    def swapIndices(self, firstIndex, secondIndex):
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
    def __init__(self, degree, index):
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
    def __init__(self, sig):
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
    
    def potentialNeighbors(self, node): #untested
        potentialNeighbors = copy.deepcopy(self.adjList)
        remList = [node.index]
        #print("len PotentialNeighbors = ", len(potentialNeighbors))
        for i in potentialNeighbors:
        #    i.print()
            if(len(i.neighbors) == i.degree):
                remList.append(i.index)
        #    else:
        #        print(False)
        #print("REMLIST AFTER FIRST PASS")
        #for i in remList:
        #    print(i)
        potentialNeighbors = [i for i in potentialNeighbors if i.index not in remList]
        #print("AFTER REMOVAL PASS")
        #for i in potentialNeighbors:
        #    i.print()
        return potentialNeighbors
        
    def currentGroupOpenEdges(self):
        #TODO: bug: for some reason, the neighborhood printed within this fn doesn't match WorkingNode's neighborhood as printed just before the call
        #start node has its neighbors, but the neighbors don't include startnode. Very strange. 
        #print("inCGOE, selfSig = ")
        #self.debug()
        currentGroup = []
        startNode = self.adjList[0]
        currentGroup.append(startNode)
        for i in startNode.neighbors:
            currentGroup.append(self.adjList[i.index])
            
        #print("Start node Neighbors = ",startNode.neighbors[1])
            
        for i in currentGroup:
            for j in i.neighbors:
                #print("j = ")
                #j.print()
                included = False
                for k in currentGroup:
                    if k.index == j.index:
                        included = True
                if included == False:
                    currentGroup.append(self.adjList[j.index])
                #if j not in currentGroup: #problem is probably here due to overloaded node equals comparitor, check index instead
                #    currentGroup.append(self.adjList[j.index]) #not sure if this works as intended, make sure it checks all neighbors of sn's nbrs recursively
        openEdges = 0
        #print("inCGOE")
        for i in currentGroup:
            #i.print()
            #print("open edges:", i.numUnfilledNbrs())
            openEdges += i.numUnfilledNbrs()
            
        #print("last inCGOE")
        #self.debug()
        return openEdges
    
    def disconnectedGroupCheck(self): 
        #TODO: bug: doesn't actually check for disconnected groups, returns true for a dc'd triangle[2,2,2] and g0[1,1] for [2,3]
        #if currentGroupOpenEdges = 0 and unfilledNodes > 0 then return True
        #currentGroup: start with 0, add all neighbors, add all neighbors of neighbors, sum numUnfilledNbrs for each in list
        #print("entered DGC: selfSig = ")
        #self.debug()
        workingGroupOpenEdges = self.currentGroupOpenEdges()
        totalOpenEdges = 0
        for i in self.adjList:
            totalOpenEdges += i.numUnfilledNbrs()
        if workingGroupOpenEdges == 0 and totalOpenEdges > 0:
            #print("DINGDINGDINGDING")
            return True
        #print("WGOE: ", workingGroupOpenEdges)
        check = False
        for i in self.adjList:
            #print("IN DCGROUPCHECK, i.ind = ", i.index, "#POTNBRS = ", len(self.potentialNeighbors(i)), "UNFILLEDNBRS = ", i.numUnfilledNbrs())
            if len(self.potentialNeighbors(i)) < i.numUnfilledNbrs():
                check = True
        return check
            
    def debug(self):
        print(self.sig)
        print("num Edges = ", self.numEdges)
        print("num Nodes = ", self.numNodes)
        for i in self.adjList:
            i.print()

    def g0Equivalent(self, edgeListOne, edgeListTwo):
        #compare sorted list of all edges by degree, return true if identical (disregarding order) else false
        degreeEdgeListOne = []
        degreeEdgeListTwo = []
        for i in edgeListOne:
            degreeEdgeListOne.append([self.adjList[i[0]].degree, self.adjList[i[1]].degree])
        for i in edgeListTwo:
            degreeEdgeListTwo.append([self.adjList[i[0]].degree, self.adjList[i[1]].degree])
        print("degEL1: ")
        for i in degreeEdgeListOne:
            print(i)
        print("degEL2: ")
        for i in degreeEdgeListTwo:
            print(i)
            
        counterL1 = Counter(map(tuple, degreeEdgeListOne))  # Convert inner lists to tuples to make them hashable
        counterL2 = Counter(map(tuple, degreeEdgeListTwo))
        
        # Check if every pair in l1 is present in l2 with the required count
        for pair, count in counterL1.items():
            if counterL2[pair] < count:
                return False
        return True
          
    def sortNodesByDegree(self):
        #returns a list of all node groups (sorted by degree) with two or more members
        nodeGroups = []
        for i in range(len(self.sig) - 1, -1, -1):
            #if self.sig[i] >= 2: #TODO: probably remove this check so we can get the full string permutation
            nodeGroups.append([])
            for j in self.adjList:
                if j.degree == i + 1:
                    nodeGroups[-1].append(j.index) #TODO: Change to append indices instead of nodes themselves #TODO is done, I think
        #for i in nodeGroups:
        #    for j in i:
        #        j.print()
        #    print()
        return nodeGroups
        
    def isomorphismTest(self, edgeListOne, edgeListTwo, swappablePairs):
        #TODO: this implementation doesn't work for all cases. Worst case scenario, we'll have to check every permutation of nodes in each 
        #equivalence group. Maybe we can analyze the approach we took to generating the edgelists and come up with something more efficient, though.
        #test for isomorphism by attempting all applicable (grouped by degree) relabeling schemes of one swap (TODO:is this sufficient?)
        #swap all swappable pairs in edgeListTwo and test for equivalence, return false otherwise
        for swapPair in swappablePairs:
            firstIndex = swapPair[0].index
            secondIndex = swapPair[1].index
            
            edgeListTwo.swapIndices(firstIndex, secondIndex)
            #for i in edgeListTwo:
            #    if i[0] == firstIndex:
            #        i[0] = 'n'
            #    if i[1] == firstIndex:
            #        i[1] = 'n'
            #    if i[0] == secondIndex:
            #        i[0] = 'm'
            #    if i[1] == secondIndex:
            #        i[1] = 'm'

            #for i in edgeListTwo:
            #    if i[0] == 'n':
            #        i[0] = secondIndex
            #    if i[1] == 'n':
            #        i[1] = secondIndex
            #    if i[0] == 'm':
            #        i[0] = firstIndex
            #    if i[1] == 'm':
            #        i[1] = firstIndex #swapPair indices in edgeListTwo now swapped
            
            if edgeListTwo.sameListDifferentOrderCheck(edgeListOne): #if the two lists are identical disregarding order
                return True
            edgeListTwo.swapIndices(firstIndex, secondIndex) #swap back for a clean slate for other checks

        return False #edgeListOne did not match any edgeListTwo after all applicable swaps
        
    def removeIsomorphicEdgeLists(self, masterEdgeLists):
        #TODO: begin here
        #check seems to work, now we need to filter out one of final configs for which true is returned in above check since they're isomorphic
        #need to check every edgeList against every succeeding edgelist in the list of edgelists (var called edgelists)
        #use list comprehension recipie found in below line
        #    edgeLists = [edgeLists[i] for i in range(len(edgeLists)) if not remList[i]]
        #remember to break and flag for removal if SLDOC returns true for any permutation 
        #everything is getting removed upon running, I need to add a check to ensure I'm not comparing a list to itself
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
            #print("final configs, ", i)
            finalConfigSet.append(EdgeList(i))
            #finalConfigSet.append(i)
                    
        finalConfigSet = removeEdgeListCopies(finalConfigSet)
        #finalConfigSet = set(finalConfigSet)  
        
        #for i in finalConfigSet:
            #print("Final config set: ")
            #i.print()
        if len(finalConfigSet) > 1:
            finalConfigSet = self.removeIsomorphicEdgeLists(finalConfigSet)
        for i in finalConfigSet:
            self.configs.append(i)
        #print("Post ismorphic edgelist removal:")
        print(self.sig, ": ", len(finalConfigSet)) 
        #for i in finalConfigSet:
            #i.print() #used to verify configs generated, all pass as of 2/6/25
        
        #nodeGroups = self.sortNodesByDegree()
        #gp = groupedPermutations(nodeGroups)
        #filteredEdgeLists = []
        #for perm in gp:
        #    filteredEdgeLists.append(filterEdgeListByPermutation(finalConfigSet[1].edgeList, perm))
        #for i in filteredEdgeLists:
        #    print(finalConfigSet[0].sameListDifferentOrderCheck(EdgeList(i)))
        
        #check seems to work, now we need to filter out one of final configs for which true is returned in above check since they're isomorphic
        
        #1/20/25 11:35 just got it working for [1,3,1], now I need to make it programmatic
        #and test all known sigs then we will know it actually works
        #first group all configs by g0 eq classes, then for all configs in the same eq class,
        #generate permutationList, filter by permutationList, and use sameListDifferentOrderCheck
        #remove any cases where true is returned and we will be left with all non-isomorphic configs of a given sig
        #a significant contribution to mathematics. Listened to Blue Train as I reached the final steps
        
        #for i in gp:
        #    print(i)
        #print("node groups:")
        #for i in nodeGroups:
        #    for j in i:
        #        print(j)
        #    print()
        #print(nodeGroups)
        
        #genSwappablePairs(nodeGroups) #depreciated
        #print("edgeLists[0] G0 Equiv to edgelists[1]:")
        #print(self.g0Equivalent(finalConfigSet[0].edgeList, finalConfigSet[1].edgeList))
        #while(True):    
        #    workingNode = workingList.pop(0)
        #    nbrhdCombinations = genNbrCombinations(workingList, workingNode.numUnfilledNbrs())
        #    cnxnList = []

 #           for potentialNbrCombination in nbrhdCombinations:
 #               self.connectToPotentialNbrs(workingNode, workingList, potentialNbrCombination, workingSig, cnxnList)
 #               #workingSig = copy.deepcopy(self)

 #               if workingSig.completionCheck == True:
 #                   print("Config Complete")
 #                   break
 #               elif workingSig.disconnectedGroupCheck == True:
 #                   print("Invalid Config")
 #                   break
 
    def identifyWorkingNode(self, workingSig):
        #returns the index of the first node in workingSig with fewer neighbors than its degree would imply
        workingNode = None
        for i in workingSig.adjList:
            if i.numUnfilledNbrs() > 0:
                workingNode = i
                #print("in identifyWN: wn = ")
                #workingNode.print()
                #print()
                return workingNode.index
     
    def iterate2(self, workingSig, cnxnList, configList, level, debug):
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
        #print("Working Node = ")
        #wn.print()
        nbrhdCombinations = genNbrCombinationsNode(workingSig.adjList, wn)
        #print("Potential Nbrhd Combinations: ")
        #for i in nbrhdCombinations:
        #    for j in i:
        #        j.print()
        #    print()
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
                    #configList.append(list(cnxnList + crc))
                    if debug: print("in graph complete, nbrhds remaining, crc = ")
                    for i in crc:
                        if debug: print(i)
                    if debug: print("Current workingSig = ")
                    workingSig.debug()
                    workingSig.deleteEdgeList(workingSig, crc) #remove current round connections from group
                    if debug: print("post delete edgeList")
                    workingSig.debug()
                    #crc = [] #reset currentRoundConnections after deleting from group
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
        #for i in configList:
            #print("final ConfigList = ", i)
        if debug: print("END of iterate2")
        return[False, cnxnList + crc, configList]
       
            
    def iterate(self, workingSig, workingList, cnxnList):
        failCase = False
        workingNode = None 
        configList = []
        currentRoundConnections = []
        for i in workingSig.adjList:
            if i.numUnfilledNbrs() > 0:
                workingNode = i
                print("WN = ")
                workingNode.print()
                print()
                break
        print("WorkingSig.complete = ", workingSig.completionCheck())
        nbrhdCombinations = genNbrCombinationsNode(workingSig.adjList, workingNode)
        print("Potential Combinations: ")
        for i in nbrhdCombinations:
            for j in i:
                j.print()
            print()
        for comb in nbrhdCombinations:
            print("checking combination: ")
            for j in comb:
                j.print()
            for node in comb:
                connect(workingSig, workingNode, node)
                currentRoundConnections.append([workingNode.index, node.index])
            print("FirstCheck in loop")
            for i in workingSig.adjList:
                i.print()
            if workingSig.completionCheck() == True:
                print("BANG config complete, cnxnList = ")
                for i in cnxnList + currentRoundConnections:
                    print(i)
                if comb != nbrhdCombinations[-1]: #(not equal to final comb to check) then deleteEdgeList like in dcg failcase
                    workingSig.deleteEdgeList(workingSig, currentRoundConnections)
                    currentRoundConnections = []
                return [True, cnxnList + currentRoundConnections]
            elif workingSig.disconnectedGroupCheck() == True:
                
                print("invalid path, CRCs = ", currentRoundConnections)
                workingSig.deleteEdgeList(workingSig, currentRoundConnections) #undo the most recent round of connections
                print("POST DELETEEDGELIST")
                for i in workingSig.adjList:
                    i.print()
                failCase = True
                #return[False]
            else:
                input()
                retVal = self.iterate(workingSig, workingList, cnxnList + currentRoundConnections)
                if retVal is not None and retVal[0] == True:
                    configList.append(retVal[1])
            print("Should be clearing workingSig and CRCs here, end of loop")
            print("current neighborhood = ")
            for x in comb:
                x.print()
            print("nbrhdCombinations[-1] = ")
            for x in nbrhdCombinations[-1]:
                x.print()
            if not failCase and comb != nbrhdCombinations[-1]: #TODO: and i == nbrhdCombinations[-1] #TODO: need to add an additional check here for successful config creation with remaining combs to check
                print("CLEARING WORKINGSIG")
                workingSig = copy.deepcopy(self)
            currentRoundConnections = []
            #clear out currentRoundConnections here
            
            
    def deleteEdgeList(self, workingSig, edgeList):
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

    def connectToPotentialNbrs(self, workingNode, workingList, nbrList, workingSig, cnxnList):
        for potentialNbr in nbrList:
            connect(workingSig, workingNode, potentialNbr)
            cnxnList.append([workingNode.index, potentialNbr.index])
            
    def genConfigs(self, level):
        #almost there, works recursively to build a single config, now we just need to add a check for a completed or invalid config
        #and iterate through all possible nbrhdCombinations, then it should be actually fucking done
        #also need to figure out how reconstruct valid configs from partial adj lists, try using a "connectionList" which gets passed back and 
        #appended to itself
        #11/7/24 Okay, we've coded most of the above, just need to implement it properly. Now the innermost nested iteration will, upon a 
        #successful completion check, add its current connections to cnxnList. We want to then return cnxnList to its immediate outer calling 
        #level, add the returned cnxnList to the outer level's cnxnList and repeat that process until we reach level 0, where we will add it to
        #the original nbrhdCombination cnxnList. After that, we want to add that final cnxnList to a list of valid configs, then continue to 
        #iterate through all possible nbrhdCombinations. Should be done after that. 
        print("Level = ", level)
        workingSig = copy.deepcopy(self)
        workingList = copy.deepcopy(workingSig.adjList)
        print("WorkingList = ")
        for i in workingList:
            i.print()
        workingNode = workingList.pop(0)
        nbrhdCombinations = genNbrCombinations(workingList, workingNode.numUnfilledNbrs())
        cnxnList = []
        completeCnxnLists = []
        print("nbrhdCombinations = ")
        for i in nbrhdCombinations:
            for j in i:
                j.print()
            print()
            
        for x in nbrhdCombinations:
            workingCombo = x
            for i in workingCombo:
                print (workingNode.index, i.index)
                print("adding ",[workingNode.index, i.index], "to list")
                cnxnList.append([workingNode.index, i.index])
                print("checking former operation: cnxnList[#cnxnList] = ", cnxnList[len(cnxnList) - 1], "workingNode.index = ", workingNode.index, "level = ", level, "i.index = ", i.index, "wn.i - l = ", workingNode.index - level)
                connect(workingSig, workingNode.index - level, i.index - level)
                for i in cnxnList:
                    print(i)

            print("CNXN List len = ", len(cnxnList))
            if workingSig.completionCheck() == True: #tested, works
                print ("Complete!")
                #for i in workingCombo:
                    #cnxnList.append([workingNode.index, i.index])
                #print("After WC Print")
                #return True + workingCombo #? (probably want to send back WorkingSig here and combine with level - 1.workingSig
                return([True, cnxnList, workingSig])
            else:
                if self.disconnectedGroupCheck() == True: #tested, seems to work
                    print("Disconnected group formed, invalid path")
                    #return False #?
                    return False

            for n in workingSig.adjList:
                n.print()

            level += 1
            #have below line return to retVal (or a better name), if retVal[0] = True, then add to FinalCnxnList
            topNode = workingSig.adjList.pop(0)
            returnInfo = workingSig.genConfigs(level) #assign result to variable to check and combine valid adjLists.
            if returnInfo[0] == True:
                cnxnList = cnxnList + returnInfo[1]
                
                print("complete cnxnList:")
                for i in cnxnList:
                    print(i)
                completeCnxnLists.append(list(cnxnList))
                cnxnList = []
                
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
        #for i in secondPassCombinations:
        #    print(i)
        return secondPassCombinations
        
    def loadAdjFromConfig(self, edgeList):
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
                #print("Config changed, new config = ")
                #self.debug()
                xNodes = [i for i in self.adjList if i.degree == pair[0]]
                yNodes = [i for i in self.adjList if i.degree == pair[1]]
                for xNode in xNodes:
                    for yNode in yNodes:
                        if xNode.index != yNode.index: #we skip evaluating instances where x and y are the same nodes
                            #print("comparing:")
                            #xNode.print()
                            #yNode.print()
                            xyDisconnected = True #assume true and invalidate otherwise
                            for nbr in xNode.neighbors:
                                #print("Neighbor comparison: nbr.index = ", nbr.index, "yNode.index = ", yNode.index)
                                if nbr.index == yNode.index: #if one of x's neighbors shares y's index they they are connected
                                    xyDisconnected = False
                            if xyDisconnected == True:
                                #print("concluding True", pair)
                                for entry in potPairBools:
                                    if entry[0] == pair:
                                        entry[1] = True
                                break                   
                        if xyDisconnected == True:
                            break
                if xyDisconnected == True:
                    break
                else:
                    #print("concluding False", pair)  #if xyDC'd has never been true by the end of all configs
                    for entry in potPairBools:      #then nodes of deg x and deg y are implicitly connected
                        if entry[0] == pair:
                            entry[1] = entry[1] or False #accoutns for cases when final check returned false after earlier returned true
        #for i in potPairs:
            #print(i)
        #for i in potPairBools:
            #print(i)
        connectablePairs = [potPairs[i] for i in range(len(potPairs)) if potPairBools[i][1] == True] #list comprehension to remove false potPairs 
        return connectablePairs
                            
    #if xyDisconnected is False, then for that configuration, x, and y, validPair is false. If any instance of a given config, x, and y 
    #show that xyDisconnected is True, then the pairbool for that pair should be true, no more search is needed for that entire pair
    #so we should be able to break out until the next Pair is being evaluated
    
    def findConnectablePairs2(self):
    #assumes all valid configs are loaded into self.configs (i.e. genAllConfigs() has been run on the same sig
        self.loadAdjFromConfig(self.configs[0].edgeList)
        potPairs = list(self.totalPotentialConnectablePairs())
        print("potPairs = ", potPairs)
        potPairBools = []
        for pair in potPairs:
            print("currentPair = ", pair)
            validPair = False
            xNodes = []
            yNodes = []
            for i in self.adjList:
                if i.degree == pair[0]:
                    xNodes.append(i)
                if i.degree == pair[1]:
                    yNodes.append(i)
            print("xNodes:")
            for i in xNodes:
                i.print()
            print("yNodes:")
            for i in yNodes:
                i.print()
            for config in self.configs:
                #config.print()
                self.loadAdjFromConfig(config.edgeList)
                self.debug()
                for xNode in xNodes:
                    print("currentXNode = ", xNode.index)
                    for yNode in yNodes:
                        #validPair = validPair or False
                        print("currentYNode = ", yNode.index)
                        if xNode.index == yNode.index: #for cases where potPair[0] = potPair[1] we ignore comparisons of nodes to themselves (since they are 
                        #both xNodes and yNodes, they will be compared to themselves)
                            print("indices match, xNode.index = ", xNode.index, "yNode.index = ", yNode.index)
                            
                        else:
                            print("indices do not match, xNode.index = ", xNode.index, "numXNbrs = ", len(xNode.neighbors), "yNode = ", yNode.index)
                            yInXNbrhd = False
                            for nbr in xNode.neighbors:
                                print("currentXNode = ", xNode.index, "yNode = ", yNode.index)
                                print("Comparing:", nbr.index, " and", yNode.index)
                                if nbr.index == yNode.index:
                                    yInXNbrhd = True
                                    print("VALID PAIR FOUND: ", xNode.index, ", ", yNode.index)
                            if yInXNbrhd == False:
                                validPair = True
                            #yNode.index not in self.adjList[xNode.index].neighbors:
                            #this means there is a node of degree = pair[1] not in the neighborhood of a node of degree = pair[0]
                            #therefore they are a valid connectable pair because there exists at least one config s.t. a node of deg = pair[0] 
                            #isn't already (and necessarily) connected to all nodes of deg = pair[1]
                            #validPair = True
            potPairBools.append(validPair)
        print("potPairs:")
        for i in potPairs:
            print(i)
        print("potPairBools:")
        for i in potPairBools:
            print(i)
        connectablePairs = [potPairs[i] for i in range(len(potPairs)) if potPairBools[i]] #list comprehension to remove false potPairs 
        return connectablePairs

            
testSigs = [[2],[2,1],[0,3],[2,2],[0,4],[1,2,1],[3,0,1],[0,2,2],[0,0,4],[2,3],[0,5],[3,1,1],[4,0,0,1],[2,1,2],[1,3,1],[2,2,0,1],[1,2,1,1],[0,4,0,1],[1,1,3],[0,3,2],[0,3,0,2],[1,0,3,1],[0,2,2,1],[0,1,4],[0,1,2,2],[0,0,4,1],[0,0,2,3],[0,0,0,5],[0,4,2],[0,0,6]]
#above are all sigs of graphlets from 2 to 5 nodes for testing purposes. All should return one config exept for [1,3,1] and [0,3,2]
test = Signature([0,3,2]) #works
test2 = Signature([1,3,1]) #works but returns two isomorphic configs
test3 = Signature([0,4,2])#connect(test, test.adjList[0],test.adjList[1])
test4 = Signature([0,0,6])
#connect(test, test.adjList[0],test.adjList[2])
#for i in test.adjList:
#    i.print()
#test.deleteEdgeList(test, [[0,1],[0,2]])
#for i in test.adjList:
#    i.print()
#test.debug()
#print(test.adjList[0] == test.adjList[1])
#genNbrCombinations(test.adjList, 3)
#test.genConfigs(0)
#test.genAllConfigs()
#test2.genAllConfigs()
#test4.genAllConfigs()
#test5 = Signature([2,3])
#test5.genAllConfigs()
#test6 = Signature([3,0,1])
#test6.genAllConfigs()
for i in testSigs:
    testSig = Signature(i)
    testSig.genAllConfigs() #all pass 2/6/2025 (2*6 = 2+0+2*5)
    print(testSig.findConnectablePairs()) #all pass 2/14/25 (2*(1+4) = 2*5)
#test5 = Signature([1,1,3])
#test6 = Signature([3,1,1])
#test6.genAllConfigs()
#print (test6.findConnectablePairs())
