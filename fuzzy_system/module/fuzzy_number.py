from .fuzzy_set import DiscreteFuzzySet

class DiscreteFuzzyNumber(DiscreteFuzzySet):
    def _combine(self, other, func):
        new_mapping = {}
        for value, grade in zip(self.values, self.grades):
            for other_value, other_grade in zip(other.values, other.grades):
                new_value = func(value, other_value)
                new_grade = min(grade, other_grade)
                if new_value not in new_mapping:
                    new_mapping[new_value] = new_grade
                else:
                    new_mapping[new_value] = max(new_mapping[new_value], new_grade)

        return DiscreteFuzzyNumber([(b,a) for a,b in sorted(new_mapping.items())])
      
    def __add__(self, other):
        if self == other:
            return self.transform(lambda x: x + x)
        return self._combine(other, lambda a,b: a+b)
    def __sub__(self, other):
        if self == other:
            return self.transform(lambda x: x - x)
        return self._combine(other, lambda a,b: a-b)
    def __mul__(self, other):
        if self == other:
            return self.transform(lambda x: x * x)
        return self._combine(other, lambda a,b: a*b)
    def __truediv__(self, other):
        if 0 in other.values:
            raise ZeroDivisionError
        if self == other:
            return self.transform(lambda x: x / x)
        return self._combine(other, lambda a,b: a/b)
    def __pow__(self, num):
        return self.transform(lambda x: x ** num)
