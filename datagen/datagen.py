import json, os
import importlib.util
from importlib import import_module


class Generate:
    def __init__(self, generator_paths):
        self._db = {}
        self.load_package_generators()
        self.load_custom_generators(generator_paths)

    def load_package_generators(self):
        package_path = os.path.dirname(__file__) + '/generators'
        files = os.listdir(package_path)
        modules = [f[:-3] for f in files if self.is_module(f)]
        for module in modules:
            self.load_package_generator(module)

    def load_custom_generators(self, generator_paths):
        for path in generator_paths:
            try:
                files = os.listdir(path)
            except FileNotFoundError:
                print(path + 'is not a valid path')
                continue
            modules = [f[:-3] for f in files if self.is_module(f)]
            for module in modules:
                self.load_custom_generator(path, module)

    def load_package_generator(self, generator):
        module = import_module('datagen.generators.' + generator)
        try:            
            self._db[generator] = getattr(module, generator)()
        except AttributeError:
            pass

    def load_custom_generator(self, path, generator):
        spec = importlib.util.spec_from_file_location(
            generator, path + '/' + generator + '.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        try:
            self._db[generator] = getattr(module, generator)()
        except AttributeError:
            pass
    
    def is_module(self, file_name):
        return file_name != '__init__.py' and file_name[-3:] == '.py'

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
