# No Tree class, a Tree is basically nodes referencing each other
class TreeNode:
    def __init__(self, data, children=[],h=0):
        self.data = data
        self.children=children
        self.height = h  # height is currently not used, it is kept in the code for possible use in the future

    def __str__(self):
        string = self.data
        return string

    def set_child(self, child):
        self.children = [child]
        child.height = self.height + 1

    def set_children(self, left, right):
        self.children = [left, right]
        left.height = self.height + 1
        right.height = self.height + 1


def CTL_conversion(root: TreeNode):  # Take the root of the tree as input
    # Check if there are syntax that can be converted
    frontier = []
    if root.data == "IMPLIES":  # Translate D->C into "not(D) OR C"
        root.data = "OR"
        temp = root.children[0]
        temp2 = root.children[1]
        negation = not_of(temp)
        root.set_children(negation,temp2)
        frontier.append(temp)
        frontier.append(temp2)
    if root.data == "AX":
        root.data = "NOT"
        temp = root.children[0]
        negation = not_of(temp)
        exist_next = TreeNode("EX")
        root.set_child(exist_next)
        exist_next.set_child(negation)
        frontier.append(temp)
    if root.data == "EF":
        ef2eu(root,frontier)
    if root.data == "AG":
        ef = TreeNode("EF")
        temp = root.children[0]
        root.set_child(ef)
        ef.set_child(temp)
        root.data="NOT"
        ef2eu(ef,frontier)
    if root.data == "AU":
        p1 = root.children[0]
        p2 = root.children[1]
        notp1 = not_of(p1)
        notp2 = not_of(p2)
        theAnd = and_of(notp1, notp2)
        eu = eu_of(notp2, theAnd)
        eg = eg_of(notp2)
        theOr = or_of(eu, eg)
        root.data = "NOT"
        root.set_child(theOr)
        frontier.append(p1)
        frontier.append(p2)
    if root.data == "EG":
        root.data="NOT"
        af = TreeNode("AF")
        temp = root.children[0]
        root.set_child(af)
        af.set_child(not_of(temp))
        frontier.append(temp)
    else:
        for i in root.children:
            frontier.append(i)
    # ***** recursive call for all children of the root *****
    if frontier:
        for i in frontier:
            CTL_conversion(i)
    return 0

# methods that are called by CTL_conversion

def ef2eu(node: TreeNode, frontier):
    node.data = "EU"
    temp = node.children[0]
    tru = TreeNode("TRUE")
    node.set_children(tru, temp)
    frontier.append(temp)

# Operators are nodes in this data structure, below are functions that make "Operator Nodes"
# It's here to make coding easier
def not_of(node: TreeNode):
    # take a node as input, return a node whose data is "not" and have the input node as single child
    negation=TreeNode("NOT")
    negation.set_child(node)
    return negation

def and_of(phi1:TreeNode,phi2:TreeNode):
    AND=TreeNode("AND")
    AND.set_children(phi1,phi2)
    return AND

def or_of(phi1:TreeNode,phi2:TreeNode):
    OR=TreeNode("OR")
    OR.set_children(phi1,phi2)
    return OR

def eu_of(phi1:TreeNode,phi2:TreeNode):
    eu=TreeNode("EU")
    eu.set_children(phi1,phi2)
    return eu

def eg_of(node: TreeNode):
    eg=TreeNode("EG")
    eg.set_child(node)
    return eg

def af_of(node: TreeNode):
    af=TreeNode("AF")
    af.set_child(node)
    return af

def ex_of(node: TreeNode):
    ex=TreeNode("EX")
    ex.set_child(node)
    return ex

def ef_of(node: TreeNode):
    res=TreeNode("EF")
    res.set_child(node)
    return res

def ag_of(node: TreeNode):
    res=TreeNode("AG")
    res.set_child(node)
    return res

def au_of(node: TreeNode, node2: TreeNode):
    res=TreeNode("AU")
    res.set_children(node, node2)
    return res

def ax_of(node: TreeNode):
    res=TreeNode("AX")
    res.set_child(node)
    return res

def implies_of(node: TreeNode, node2: TreeNode):
    res=TreeNode("IMPLIES")
    res.set_children(node, node2)
    return res

# *** of-functions ENDS ***

def toString(node):
    if len(node.children)==0:
        return node.data
    if len(node.children)==1:
        return node.data+"("+toString(node.children[0])+")"
    if len(node.children)==2:
        return toString(node.children[0])+" "+node.data+" "+toString(node.children[1])


