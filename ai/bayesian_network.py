##Pr(a,b,c| d,e,f)
##= Pr(a,b,c,d,e,f) / Pr(d,e,f)
##
##Pr(d,e,f) = sum_a sum_b sum_c Pr(a,b,c,d,e,f)

class Table:
    def __init__(self, parents, table):
        n = len(parents)
        assert len(table[0]) == n + 1
        assert len(table) == 2 ** n
        
        s = set()
        for entry in table:
            assert all([entry[i] == 1 or entry[i] ==  0 for i in range(n)]), "illegal value in " + str(entry)
            s.add(tuple(entry[:n]))
        assert len(s) == 2**n, "Invalid table"
        self.parents = parents
        self.table = table

    def __repr__(self):
        s = ""

        s += ",".join(map(str, self.parents)) + "\n"

        for entry in self.table:
            s += ",".join(map(str, entry)) + "\n"
        
        return s

    def getProb(self, givens, truths, truth_value):
        assert sorted(givens) == sorted(self.parents)
        assert len(givens) == len(truths)

        indices = [self.parents.index(i) for i in givens]
        for entry in self.table:
            if all([entry[index] == t for index,t in zip(indices, truths)]):
                return entry[-1] if truth_value else 1- entry[-1]
        assert False, "No entry found"
class Node:
    def __init__(self, num):
        self.num = num
        self.parents = []
        self.children = []

    def point(self, node):
        self.children.append(node)
        node.parents.append(self)

    def __repr__(self):
        return f'Node {str(self.num)}, Children: {list(map(lambda x: x.num, self.children))}, Parents: {list(map(lambda x: x.num, self.parents))}'

class Network:
    def __init__(self, size):
        self.nodes = [Node(i) for i in range(size)]
        self.tables = [[] for i in range(size)]
    def __repr__(self):
        return "\n".join(map(str, self.nodes))

    def addTable(self, node, table):
        assert len(table.parents) == len(self.nodes[node].parents)
        self.tables[node] = table

    def calcProbGiven(self, events, given):
        assert all(map(lambda x: type(x) is str, events))

        numerator = self.calcProb(events + given)
        denominator = self.calcProb(given)

        
        print("num", numerator)
        print("dem", denominator)
        return self.calcProb(events + given) / self.calcProb(given)
    
    def calcProb(self, events):
        assert all(map(lambda x: type(x) is str, events))

        truths = [0 if event[0] == '-' else 1 for event in events]
        events = [int(event.replace('-', '')) for event in events]

        if all([len(self.nodes[event].parents) == 0 for event in events]):
            pr = 1
            for e,t in zip(events, truths):
                pr *= self.tables[e].getProb([], [], t)
            return pr
        elif len(events) == len(self.nodes):
            return self.calcFullProb(events, truths)
        else:
            missing_events = [e for e in range(len(self.nodes)) if e not in events]
            pr = 0

            for i in range(1 << len(missing_events)):
                new_truths = [(i & (1 << j)) > 0 for j in range(len(missing_events))]
                pr += self.calcFullProb(events+missing_events, truths+new_truths)
            return pr

    def calcFullProb(self, events, truths):
        order = self.getOrder()
        pr = 1

        dic = {e:t for e,t in zip(events, truths)}
        arr = []
        for node in order:
            node_num = node.num
            parent_nums = [par.num for par in node.parents]
            parent_truths = [dic[n] for n in parent_nums]
            arr.append(self.tables[node_num].getProb(parent_nums, parent_truths, dic[node_num]))
            pr *= self.tables[node_num].getProb(parent_nums, parent_truths, dic[node_num])

        print(arr)
        return pr

    def getOrder(self):
        stack = []

        visited = set()

        def DFS(node):
            if node in visited:
                return

            visited.add(node)
            for child in node.children:
                if child not in visited:
                    DFS(child)

            stack.append(node)
            
        for node in self.nodes:
            DFS(node)
            
        return stack

##        
##n = Network(5)
##n.nodes[0].point(n.nodes[1])
##n.nodes[0].point(n.nodes[2])
##n.nodes[0].point(n.nodes[3])
##n.nodes[0].point(n.nodes[4])
##
##n.addTable(0, Table([], [[1/3]]))
##n.addTable(1, Table([0], [[1, 6/10], [0, 10/20]]))
##n.addTable(2, Table([0], [[1, 7/10], [0, 12/20]]))
##n.addTable(3, Table([0], [[1, 7/10], [0, 10/20]]))
##n.addTable(4, Table([0], [[1, 9/10], [0, 2/20]]))
##
##print(n.calcProbGiven(["0"], [str(i) for i in range(1, 4)] + ["-4"]))
##print(n.calcProb(["0"] + [str(i) for i in range(1, 4)] + ["-4"]))


n = Network(4)
n.nodes[0].point(n.nodes[1])
n.nodes[0].point(n.nodes[2])

n.nodes[1].point(n.nodes[2])
n.nodes[1].point(n.nodes[3])
n.nodes[2].point(n.nodes[3])

n.addTable(0, Table([], [[0.6]]))
n.addTable(1, Table([0], [[1, 0.8], [0, 0.4]]))
n.addTable(2, Table([0, 1], [[0, 0, 0.1], [0, 1, 0.6], [1, 0, 0.4], [1,1, 0.9]]))
n.addTable(3, Table([1, 2], [[0, 0, 0.1], [1, 0, 0.2], [0, 1, 0.7], [1,1, 0.8]]))

print(n.calcProbGiven(["3"], ["0"]))
print(n.calcProbGiven(["3"], ["-0"]))
print(n.calcProbGiven(["0"], ["3"]))

##n = Network(5)
##n.nodes[0].point(n.nodes[1])
##n.nodes[1].point(n.nodes[2])
##n.nodes[3].point(n.nodes[1])
##n.nodes[3].point(n.nodes[4])
##
##n.addTable(0, Table([], [[5/6]]))
##n.addTable(1, Table([0, 3], [[1, 1, 160/220], [1, 0, 240/280], [0, 1, 10/70], [0, 0, 10/30]]))
##n.addTable(2, Table([1], [[1, 7/10], [0, 10/20]]))
##n.addTable(3, Table([], [[290/600]]))
##n.addTable(4, Table([3], [[1, 9/10], [0, 2/20]]))
##
##print(n.calcProbGiven(["-1"], ["0", "3"]))
