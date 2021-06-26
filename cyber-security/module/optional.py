"""Utility class to wrap potentially NoneType objects"""
class Optional:
    def __init__(self, value):
        self.value = value
    
    @classmethod
    def from_func(cls, func):
        try:
            return cls(func())
        except Exception:
            return cls(None)
    
    def apply(self, func):
        if self.value == None:
            return Optional(None)
        try:
            return Optional(func(self.value))
        except Exception as e:
            print(e)
            return Optional(None)
    
    def __repr__(self):
        return f"Optional({self.value})"
    
    @property
    def isEmpty(self):
        return self.value == None
    
    @staticmethod
    def map_over(func, seq):
        return map(lambda x: x.apply(func), seq)
    
    @staticmethod
    def zip_with(funcs, seq):
        return map(lambda elem: elem[1].apply(elem[0]), zip(funcs, seq))
