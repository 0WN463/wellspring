from .fuzzy_set import DiscreteFuzzySet

class DiscreteFuzzyRelation:
    """Section 1: Definition"""
    def __init__(self, a_values, b_values, table):
        assert len(table) == len(a_values)
        assert len(table[0]) == len(b_values)
        
        self.a_values = a_values
        self.b_values = b_values
        self.table = table
        
    def infer(self, fuzzy_set):        
        grades = [max([min(a,fuzzy_set.membership_dict[v]) for a, v in zip(col, self.a_values)]) for col in zip(*self.table)]
        return DiscreteFuzzySet([(grade, value) for grade,value in zip(grades, self.b_values)])
    def __repr__(self):
        string = ''
        row_format ="{:<15}" * (len(self.b_values) + 1)
        string += row_format.format("", *self.b_values) + '\n'
        string += '\n'.join([row_format.format(team, *row) for team, row in zip(self.a_values, self.table)])
        return string

    """Section 2: From Inferences"""
    @classmethod
    def from_mamdani(cls, antecedent, consequent):
        table = [[min(x, y) for x in consequent.grades] for y in antecedent.grades]
        return cls(antecedent.values, consequent.values, table)
