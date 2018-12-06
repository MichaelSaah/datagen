import json
from .generators import Generate

class datagen:
    gen = Generate()

    def __call__(self, jsn, n=1):
        d = json.loads(jsn)
        data = self.generate(d, n)
        return json.dumps(data)

    def generate(self, d, n=1):
        if n > 1:
            d = {'_n' : n, 'obj' : d}
        return self.replace_values(d)

    def replace_values(self, d):
        if isinstance(d, list):
            return list(map(self.replace_values, d))
        elif isinstance(d, dict):
            if '_n' in d:
                try:
                    n = int(d['_n'])
                except ValueError:
                    msg = f"Value given for `_n` not valid: {d['_n']} must be integer"
                    raise ValueError(msg)
                if 'obj' in d:
                    obj = d['obj']
                else:
                    msg = f"`_n` found, but `obj` not found"
                    raise ValueError(msg)
                return self.replace_values([obj for _ in range(n)])
            else:
                return {k: self.replace_values(v) for k,v in d.items()}
        elif isinstance(d, str):
            return self.gen(d)
        else:
            return d
