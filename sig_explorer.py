
class Node():

    def __init__(self, numConnections):
        self.totalConnections = numConnections
        self.activeConnections = 0
        self.connectedNodes = []
        self.terminal = False
        
    def connectNodes(node1, node2):
        if node1.terminal == False and node2.terminal == False:
            node1.connectedNodes.append(node2)    
            node1.activeConnections += 1    
            if node1.activeConnections == node1.totalConnections:
                node1.terminal = True
    
            node2.connectedNodes.append(node1)
            node2.activeConnections += 1
            if node2.activeConnections == node2.totalConnections:
                node2.terminal = True
                
    def nodeDebug(self):
        print("totalCon: ", self.totalConnections)
        print("activeCon: ", self.activeConnections)
        print("terminal: ", self.terminal)

class field():

    def __init__(self, signature):
        #signature supposed to be a list of positve ints, i.e. [3, 2, 1]
        #is the signature for a graph with three nodes of deg 1, two nodes deg 2, and one node of deg 3
        self.signature = signature
        self.unallocNodes = []
        self.allocNodes = []
        self.iterations = 0
        self.genNodesFromSig()
        
    def sigCheck(self):
        sum = 0
        index = 0
        for i in self.signature:
            sum += i * index
            
            index += 1
            
    def genNodesFromSig(self):
        indexCtr = 1
        for i in self.signature:
            while i > 0:
                self.unallocNodes.append(Node(indexCtr))
                i -= 1
            indexCtr += 1
            
    def iterate(self):
        #while t.e. nonterminal nodes
        #   if there are unallocNodes, add one such to 
        #   connected group or to another unallocNode 
        #   else connect loose nonterminal ends until none remain
        #   if one nonterminal node remains, path failure
        while len(self.unallocNodes) > 0:
            continue

    def debugField(self):
        print("Signature: ", str(self.signature))
        print("Unalloc Nodes: ")
        for i in self.unallocNodes:
            i.nodeDebug()
        print("Alloc Nodes: ")
        for i in self.allocNodes:
            i.nodeDebug()
        
foo = field([0, 3, 2])
foo.debugField()
