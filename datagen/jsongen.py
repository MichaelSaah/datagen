import copy, json
from .generators import Generate

class JsonGen:
    gen = Generate()

    def __call__(self, jsn, n):
        d = json.loads(jsn)
        data = self.generate(d, n)
        return data

    def generate(self, d, n=1):
        if n==1:
            data = self.replace_values(d)
        else:
            data = []
            for _ in range(n):
                data.append(self.replace_values(copy.deepcopy(d)))
        return data    

    def replace_values(self, d):
        if isinstance(d, list):
            return list(map(self.replace_values, d))
        elif isinstance(d, dict):
            return {k: self.replace_values(v) for k,v in d.items()}
        elif isinstance(d, str):
            return self.gen(d)
        else:
            return d
