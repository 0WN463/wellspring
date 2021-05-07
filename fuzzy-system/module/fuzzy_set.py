from collections import defaultdict

class FuzzySet:
    pass

class DiscreteFuzzySet(FuzzySet):
    """Section 1: Definition"""
    def __init__(self, value_grades):
        value_grades = list(filter(lambda x: x[0] > 0, value_grades))
        
        if len(value_grades) == 0:
            self.values = []
            self.grades = []
            return
        
        grades, values = zip(*value_grades)
        self.values = values
        self.grades = grades
    
    @classmethod
    def from_string(cls, string, value_type=int):
        return cls([(float(frag.split('/')[0]), (value_type(frag.split('/')[1]))) for frag in string.split('+')])
            

    def __repr__(self):
        if len(self.grades) == 0:
            return 'Empty'
        return ' + '.join([f'{g:.3g}/{v:.3g}' for g,v in sorted(zip(self.grades, self.values), key=lambda x: x[1])])

    def get_grade(self, value):
        return self.membership_dict[value]

    @property
    def membership_dict(self):
        return defaultdict(float, {v:g for g,v in zip(self.grades, self.values)})

    @property
    def height(self):
        return max(self.grades)

    @property
    def is_normal(self):
        return self.height == 1

    @property
    def support(self):
        return self.values

    @property
    def core(self):
        return [v for v,g in zip(self.values, self.grades) if g == 1]

    @property
    def cardinality(self):
        return sum(self.grades)

    @property
    def relative_cardinality(self):
        return self.cardinality/len(self.grades)


    """Section 2: Operations"""
            
    def union(self, other):
        values = set(self.membership_dict.keys())
        values.update(other.membership_dict.keys())
        return DiscreteFuzzySet([(max(self.membership_dict[val], other.membership_dict[val]), val) for val in values])
    
    def intersection(self, other):
        values = set(self.membership_dict.keys())
        values.update(other.membership_dict.keys())
        return DiscreteFuzzySet([(min(self.membership_dict[val], other.membership_dict[val]), val) for val in values])
   
    """Section 3: Cuts"""
    def alpha_cut(self, grade):
        return [v for v, g in zip(self.values, self.grades) if g >= grade]

    def strong_alpha_cut(self, grade):
        return [v for v, g in zip(self.values, self.grades) if g > grade]

    @property
    def level_set(self):
        return sorted(set(self.grades))

    """Section 4: Transformation"""

    def transform(self, func):
        new_mapping = defaultdict(float)
        
        for value, grade in zip(self.values, self.grades):
            value = func(value)
            new_mapping[value] = max(new_mapping[value], grade)
    
        return DiscreteFuzzySet([(b,a) for a,b in sorted(new_mapping.items())])

    def center(self):
        return sum([grade*value for value,grade in self.membership_dict.items()])/sum(self.grades)
    
