import json, os
from importlib import import_module

class Generate:
    def __init__(self, generator_paths):
        generator_paths.append(os.path.dirname(__file__) + '/generators')
        self._db = {}
        for path in generator_paths: 
            for module in os.listdir(path):
                if module == '__init__.py' or module[-3:] != '.py':
                    continue
                generator = module[:-3]
                try:            
                    module = import_module('datagen.generators.' + generator)
                    self._db[generator] = getattr(module, generator)()
                except AttributeError:
                    continue

    def __call__(self, args_str):
        args_out = dict() 
        args = args_str.split('|')

        # validate call and call args
        if args[0] not in self._db:
            msg = f"Invalid data type given: {args[0]}"
            raise ValueError(msg)

        if len(args) > 1:
            return self._db[args[0]](*args[1:])
        else:
            return self._db[args[0]]()


class Datagen:
    def __init__(self, generator_paths=[]):
        self.gen = Generate(generator_paths)

    def __call__(self, data, n=1, native=False): 
        if native:
            return self.generate(data, n)
        else:
            data = json.loads(data)
            data = self.generate(data, n)
            return json.dumps(data)

    def generate(self, d, n):
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
