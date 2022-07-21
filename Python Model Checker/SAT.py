import CTL

class State:    # Graph is simply list of states
    def __init__(self, atoms, name: str, nextStates=[]):  # atoms is a "list of Atom
        self.atoms = atoms  # list of atoms
        self.nextStates = nextStates  # list of next states
        self.name=name  # Currently it's just help printing out the results

    def __str__(self):
        return self.name

    def setNext(self,states):
        self.nextStates=states
        return

class Graph(list):
    def __init__(self, *args):
        super(Graph, self).__init__(args)

    def __sub__(self, other):
        return self.__class__(*[item for item in self if item not in other])

    def intersection(self, list2):
        res=Graph()
        for i in self:
            if i in list2:
                res.append(i)
        return res

    def union(self, lst2):
        summation= self + lst2
        res=Graph()
        for i in summation:
            if i not in res:
                res.append(i)
        return res

    def __str__(self):
        res="["
        for i in self:
            res=res+str(i)+","
        if len(res)>1:
            res=res[:-1]
        res+="]"
        return res

def ModelChecking(CTL_formula: CTL.TreeNode, transition_system: Graph):
    CTL.CTL_conversion(CTL_formula)
    res=SAT(CTL_formula,transition_system)
    return res

def SAT(phi: CTL.TreeNode, graph:Graph)->Graph:
    if phi.data=="TRUE":
        return graph
    if phi.data=="FALSE":
        return None
    if phi.data=="NOT":
        return graph-SAT(phi.children[0],graph)
    if phi.data=="AND":
        a=SAT(phi.children[0],graph)
        b=SAT(phi.children[1],graph)
        return a.intersection(b)
    if phi.data=="OR":
        a=SAT(phi.children[0],graph)
        b=SAT(phi.children[1],graph)
        return a.union(b)
    if phi.data=="EX":
        return SATex(phi.children[0],graph)
    if phi.data=="AF":
        return SATaf(phi.children[0],graph)
    if phi.data=="EU":
        return SATeu(phi.children[0],phi.children[1],graph)
    else:    # in every other cases, we treat the input string as atomic
        res=Graph()
        for i in graph:
            if phi.data in i.atoms:
                res.append(i)
        return res

def SATex(phi: CTL.TreeNode, S: Graph):
    X=SAT(phi,S)
    Y=PreE(X,S)
    return Y

def SATaf(phi: CTL.TreeNode, S:Graph):
    X=S
    Y=SAT(phi,S)
    while Y != X:
        X=Y
        Y=Y.union(PreA(Y,S))
    return Y

def SATeu(phi: CTL.TreeNode,phi2: CTL.TreeNode,S:Graph):
    W=SAT(phi,S)
    X=S
    Y=SAT(phi2,S)
    while Y != X:
        X=Y
        Y=Y.union(W.intersection(PreE(Y,S)))
    return Y

def PreE(Y:Graph, G:Graph):  # Y is not technically "Graph", set of states
    # but in this data structure, Graph is simply list of states. So we say Y is graph
    X=Graph()
    for i in G:
        for j in i.nextStates:
            if (j in Y) and (i not in X):
                X.append(i)
    return X

def PreA(Y:Graph, G: Graph):
    return G-PreE(G-Y, G)  # the equation from the book





