import copy, json
from .generators import Generate

class JsonGen:
    gen = Generate()

    def __call__(self, jsn, n):
        d = json.loads(jsn)
        data, _ = self.generate(d, n)
        return data

    def generate(self, d, n=1):
        if n==1:
            data = self.replace_values(d)
            cost = self.calculate_cost(d)
        else:
            data = []
            cost = 0
            for _ in range(n):
                data.append(self.replace_values(copy.deepcopy(d)))
                cost += self.calculate_cost(d)
        return data, cost    

    def replace_values(self, d):
        if isinstance(d, list):
            return list(map(self.replace_values, d))
        elif isinstance(d, dict):
            return {k: self.replace_values(v) for k,v in d.items()}
        elif isinstance(d, str):
            return self.gen(d)
        else:
            return d
        
    def calculate_cost(self, d):
        cost = 0
        def cc(d):
            nonlocal cost
            if isinstance(d, list):
                return list(map(cc, d))
            elif isinstance(d, dict):
                return {k: cc(v) for k,v in d.items()}
            elif isinstance(d, str):
                cost += self.gen.cost(d)
            else:
                return d
        cc(d)
        return cost
