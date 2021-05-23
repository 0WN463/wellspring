

class LeaveNode:
    def __init__(self, value):
        self.value = value
    
class HiddenNode:
    def __init__(self, children):
        assert type(children) == list
        self.children = children

def DFS(node):
    if type(node) == LeaveNode:
        print(node.value)
    else:
        for c in node.children:
            DFS(c)

            
def max_val(node, a, b):
    if type(node) == LeaveNode:
        print("Explored: ", node.value)
        return node.value
    if type(node) != HiddenNode:
        assert "wrong type", node
    v = -1000
    for i, child in enumerate(node.children):
        v = max(v, min_val(child, a, b))
        if v >= b:
            for c in node.children[i+1:]:
                try:
                    print("Pruned at ", node.tag, c.tag)
                except:
                    print("Pruned at ", node.tag,  c.value)
            return v

        a = max(a, v)
        
    return v

def min_val(node, a, b):
    if type(node) == LeaveNode:
        print("Explored: ", node.value)

        return node.value

    if type(node) != HiddenNode:
        assert "wrong type", node
    v = 1000
    for i, child in enumerate(node.children):
        v = min(v, max_val(child, a, b))

        if v <= a:
            for c in node.children[i+1:]:
                try:
                    print("Pruned at ", node.tag, c.tag)
                except:
                    print("Pruned at ", node.tag,  c.value)
            return v

        b = min(b, v)

    return v
##
##arr = [1,1,-1,-1,-1,1,-1,1,-1,-1,1,1,]
##
##
##leaves = [LeaveNode(i) for i in arr]
##
##layer1 = []
##
##
##layer1.append(HiddenNode( [leaves[0], leaves[1]]))
##layer1.append(HiddenNode( [leaves[2], leaves[3]]))
##layer1.append(HiddenNode( [leaves[4], leaves[5]]))
##layer1.append(HiddenNode( [leaves[6], leaves[7]]))
##
##
##layer2 = []
##
##layer2.append(HiddenNode( [layer1[0], layer1[1]]))
##layer2.append(HiddenNode( [layer1[2], layer1[3]]))
##layer2.append(HiddenNode( [leaves[8], leaves[9]]))
##layer2.append(HiddenNode( [leaves[10], leaves[11]]))
##
##layer3 = []
##
##layer3.append(HiddenNode( [layer2[0], layer2[1]]))
##layer3.append(HiddenNode( [layer2[2], layer2[3]]))
##
##root = HiddenNode([layer3[0], layer3[1]])
##
##
##for i, n in enumerate(layer1):
##    n.tag = "1L" + str(i)
##
##for i, n in enumerate(layer2):
##    n.tag = "2L" + str(i)
##
##for i, n in enumerate(layer3):
##    n.tag = "3L" + str(i)
##
##root.tag = "root"
##
##print(max_val(root, -1000, 1000))
##
##



##arr = [0 for i in range(14)]
##
##leaves = [LeaveNode(i) for i in arr]
##layer1 = []
##
##
##layer1.append(HiddenNode( [leaves[0], leaves[1]]))
##layer1.append(HiddenNode( [leaves[2], leaves[3]]))
##layer1.append(HiddenNode( [leaves[6], leaves[7]]))
##layer1.append(HiddenNode( [leaves[8], leaves[9]]))
##layer1.append(HiddenNode( [leaves[10], leaves[11]]))
##layer1.append(HiddenNode( [leaves[12], leaves[13]]))
##
##
##layer2 = []
##
##layer2.append(HiddenNode( [layer1[0], layer1[1]]))
##layer2.append(HiddenNode( [leaves[4], leaves[5]]))
##layer2.append(HiddenNode( [layer1[2], layer1[3]]))
##layer2.append(HiddenNode( [layer1[4], layer1[5]]))
##
##layer3 = []
##
##layer3.append(HiddenNode( [layer2[0], layer2[1]]))
##layer3.append(HiddenNode( [layer2[2], layer2[3]]))
##
##root = HiddenNode([layer3[0], layer3[1]])
##
##for i, n in enumerate(layer1):
##    n.tag = "1L" + str(i)
##
##for i, n in enumerate(layer2):
##    n.tag = "2L" + str(i)
##
##for i, n in enumerate(layer3):
##    n.tag = "3L" + str(i)
##
##root.tag = "root"
##
##print(max_val(root, -1000, 1000))


